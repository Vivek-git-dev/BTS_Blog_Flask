from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from app.models.post import Post
from app.forms.comment_form import CommentForm
from app.forms.post_form import PostForm
from app.models.comment import Comment
from app.models.category import Category
from flask_login import login_required, current_user
from app import db
from app.utils.sanitize import sanitize_html
import html as _html

blog_bp = Blueprint("blog", __name__)

@blog_bp.route("/<slug>", methods=["GET", "POST"])
def post_detail(slug):
    post = Post.query.filter_by(slug=slug, is_published=True).first_or_404()
    
    # Increment view count
    if post.views is None:
        post.views = 0
    post.views += 1
    db.session.commit()

    form = CommentForm()
    # If an anonymous user tries to POST a comment, redirect to login early
    if request.method == 'POST' and not current_user.is_authenticated:
        flash("Please log in to comment.", "warning")
        return redirect(url_for("auth.login", next=request.path))

    # Handle comment submission
    if form.validate_on_submit():

        # Unescape any HTML entities (e.g. &lt;p&gt;) then sanitize before saving
        raw_comment = form.content.data or ""
        unescaped_comment = _html.unescape(raw_comment)
        safe_content = sanitize_html(unescaped_comment)

        new_comment = Comment(
            content=safe_content,
            user_id=current_user.id,
            post_id=post.id,
        )
        db.session.add(new_comment)
        db.session.commit()

        flash("Comment added successfully!", "success")
        return redirect(url_for("blog.post_detail", slug=slug))

    # Render the post + comments + form
    return render_template("post.html", post=post, form=form)

@blog_bp.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()

    # Only admin role may create posts
    if getattr(current_user, 'role', None) != 'admin':
        flash("You do not have permission to create posts.", "warning")
        return redirect(url_for("main.home"))

    # Populate category choices dynamically
    form.categories.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():

        raw_html = (form.content.data or "").strip()
        # If the editor or user submitted escaped HTML entities (e.g. &lt;p&gt;),
        # unescape them first so bleach can preserve allowed tags correctly.
        unescaped_html = _html.unescape(raw_html)
        safe_content = sanitize_html(unescaped_html)

        new_post = Post(
            title=form.title.data,
            slug=form.slug.data,
            summary=form.summary.data,
            content=safe_content,
            image_url=form.image_url.data,
            author_id=current_user.id,
            is_published=form.is_published.data,
            read_time=form.read_time.data,
        )

        # Add categories (many-to-many)
        selected_ids = form.categories.data
        new_post.categories = Category.query.filter(Category.id.in_(selected_ids)).all()

        db.session.add(new_post)
        db.session.commit()

        flash("Post created successfully!", "success")
        return redirect(url_for("main.home"))

    return render_template("create_post.html", form=form,
                           title="Create New Blog Post",
                           action_url=url_for('blog.create_post'),
                           btn_label="Create Post")


@blog_bp.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    # Only admin may edit posts
    if getattr(current_user, 'role', None) != 'admin':
        flash("You do not have permission to edit posts.", "warning")
        return redirect(url_for('main.home'))

    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)

    # Populate category choices dynamically
    form.categories.choices = [(c.id, c.name) for c in Category.query.all()]

    # Pre-select categories on GET
    if request.method == 'GET':
        form.categories.data = [c.id for c in post.categories]

    if form.validate_on_submit():
        raw_html = (form.content.data or "").strip()
        unescaped_html = _html.unescape(raw_html)
        safe_content = sanitize_html(unescaped_html)

        post.title = form.title.data
        post.slug = form.slug.data
        post.summary = form.summary.data
        post.content = safe_content
        post.image_url = form.image_url.data
        post.is_published = form.is_published.data
        post.read_time = form.read_time.data

        selected_ids = form.categories.data
        post.categories = Category.query.filter(Category.id.in_(selected_ids)).all()

        db.session.commit()

        flash('Post updated successfully!', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_post.html', form=form,
                           title="Edit Blog Post",
                           action_url=url_for('blog.edit_post', post_id=post.id),
                           btn_label="Save")


@blog_bp.route('/delete-post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    if getattr(current_user, 'role', None) != 'admin':
        flash("You do not have permission to delete posts.", "warning")
        return redirect(url_for('main.home'))

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    flash('Post deleted.', 'info')
    return redirect(url_for('main.dashboard'))
