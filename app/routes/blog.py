from flask import Blueprint, render_template, abort, request
from app.models.post import Post
from app.models.category import Category

blog_bp = Blueprint("blog", __name__)


# ---------------------------
# 1. List all published posts
# ---------------------------
@blog_bp.route("/")
def list_posts():
    page = request.args.get("page", 1, type=int)

    posts = (
        Post.query.filter_by(is_published=True)
        .order_by(Post.created_at.desc())
        .paginate(page=page, per_page=6)
    )

    return render_template("blog/post_list.html", posts=posts)


# ---------------------------
# 2. View Single Post Page
# ---------------------------
@blog_bp.route("/<slug>")
def post_detail(slug):
    post = Post.query.filter_by(slug=slug, is_published=True).first()

    if not post:
        abort(404)

    return render_template("blog/post_detail.html", post=post)


# ---------------------------
# 3. List posts under a category
# ---------------------------
@blog_bp.route("/category/<category_slug>")
def posts_by_category(category_slug):
    category = Category.query.filter_by(slug=category_slug).first()

    if not category:
        abort(404)

    posts = (
        category.posts
        .filter_by(is_published=True)
        .order_by(Post.created_at.desc())
        .all()
    )

    return render_template(
        "blog/post_list.html",
        posts=posts,
        category=category
    )
