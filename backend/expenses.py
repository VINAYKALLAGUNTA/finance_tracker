# expenses.py
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from models import db, Expense
from datetime import datetime

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@expenses_bp.route('/add-expense', methods=['POST'])
@login_required
def add_expense():
    data = request.get_json()
    new_exp = Expense(
        amount=data['amount'],
        category=data['category'],
        date=datetime.strptime(data['date'], '%Y-%m-%d'),
        user_id=current_user.id
    )
    db.session.add(new_exp)
    db.session.commit()
    return jsonify({'message': 'Expense added'})

@expenses_bp.route('/view-expenses')
@login_required
def view_expenses():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    data = [{
        'id': e.id,
        'amount': e.amount,
        'category': e.category,
        'date': e.date.strftime('%Y-%m-%d')
    } for e in expenses]
    return jsonify(data)

@expenses_bp.route('/delete-expense/<int:id>', methods=['DELETE'])
@login_required
def delete_expense(id):
    exp = Expense.query.get(id)
    if exp and exp.user_id == current_user.id:
        db.session.delete(exp)
        db.session.commit()
        return jsonify({'message': 'Deleted'})
    return jsonify({'error': 'Not authorized'}), 403

@expenses_bp.route('/charts')
@login_required
def charts():
    return render_template('charts.html')


@expenses_bp.route('/charts-data')
@login_required
def charts_data():
    # Group expenses by category
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    
    summary = {}
    for exp in expenses:
        summary[exp.category] = summary.get(exp.category, 0) + exp.amount

    labels = list(summary.keys())
    values = list(summary.values())

    return jsonify({'labels': labels, 'values': values})
