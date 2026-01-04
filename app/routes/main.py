from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.post import Post
from datetime import datetime
from sqlalchemy import extract

main_bp = Blueprint('main', __name__)


def get_last_12_months():
    months = []
    today = datetime.today()
    current_year = today.year
    current_month = today.month

    for i in range(12):
        month = current_month - i
        year = current_year
        if month <= 0:
            month += 12
            year -= 1
        
        month_name = datetime(year, month, 1).strftime('%B')
        months.append({'name': month_name, 'year': year, 'month': month})
    
    return months


@main_bp.route("/")
def home():
    # Fetch the latest 10 posts, newest first
    latest_posts = (
        Post.query
        .filter_by(is_published=True)
        .order_by(Post.created_at.desc())
        .limit(10)
        .all()
    )
    
    
    last_12_months = get_last_12_months()
    
    trending_posts = (
        Post.query
        .filter_by(is_published=True)
        .order_by(Post.views.desc())
        .limit(3)
        .all()
    )

    return render_template("index.html", posts=latest_posts, months=last_12_months, trending_posts=trending_posts)


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/archives/<int:year>/<int:month>")
@login_required
def archives(year, month):
    posts = (
        Post.query
        .filter(extract('year', Post.created_at) == year)
        .filter(extract('month', Post.created_at) == month)
        .filter_by(is_published=True)
        .order_by(Post.created_at.desc())
        .all()
    )
    
    month_name = datetime(year, month, 1).strftime('%B')
    return render_template("archives.html", posts=posts, year=year, month_name=month_name)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Admin-only dashboard
    if getattr(current_user, 'role', None) != 'admin':
        flash("You do not have access to the admin dashboard.", "warning")
        return redirect(url_for('main.home'))

    q = request.args.get('q', '').strip()
    posts = None
    if q:
        posts = (
            Post.query
            .filter((Post.title.ilike(f"%{q}%")) | (Post.slug.ilike(f"%{q}%")))
            .order_by(Post.created_at.desc())
            .all()
        )

    return render_template('dashboard.html', posts=posts)
