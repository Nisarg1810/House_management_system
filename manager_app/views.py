from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db import connection, OperationalError, ProgrammingError
from datetime import datetime, date, timedelta
from .models import InventoryItem, Expense, Event, Budget

@login_required
def dashboard_view(request):
    """Main dashboard view with form handling"""
    
    # Handle form submissions
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'add_stock':
            return handle_add_stock(request)
        elif form_type == 'add_expense':
            return handle_add_expense(request)
        elif form_type == 'add_event':
            return handle_add_event(request)
        elif form_type == 'update_budget':
            return handle_update_budget(request)
    
    # Fetch data for dashboard
    context = get_dashboard_context(request.user)
    return render(request, 'manager_app/dashboard.html', context)

def handle_add_stock(request):
    """Handle adding new inventory item"""
    try:
        item_name = request.POST.get('item_name', '').strip()
        quantity = int(request.POST.get('quantity', 0))
        category = request.POST.get('category', 'Other')
        description = request.POST.get('description', '').strip()
        
        # Validation
        if not item_name:
            messages.error(request, 'Item name is required!')
            return redirect('manager_app:dashboard')
        
        if quantity <= 0:
            messages.error(request, 'Quantity must be greater than 0!')
            return redirect('manager_app:dashboard')
        
        # Check if item already exists for this user
        existing_item = InventoryItem.objects.filter(
            user=request.user, 
            item_name__iexact=item_name
        ).first()
        
        if existing_item:
            # Update existing item quantity
            existing_item.quantity += quantity
            existing_item.save()
            messages.success(request, f'Updated {item_name} quantity by {quantity}!')
        else:
            # Create new item
            InventoryItem.objects.create(
                user=request.user,
                item_name=item_name,
                quantity=quantity,
                category=category,
                description=description
            )
            messages.success(request, f'Added {item_name} to inventory!')
            
    except ValueError:
        messages.error(request, 'Please enter a valid quantity!')
    except (OperationalError, ProgrammingError) as e:
        messages.error(request, 'Database tables not found. Please run migrations: python manage.py migrate')
    except Exception as e:
        messages.error(request, f'Error adding stock: {str(e)}')
    
    return redirect('manager_app:dashboard')

def handle_add_expense(request):
    """Handle adding new expense"""
    try:
        title = request.POST.get('title', '').strip()
        amount_str = request.POST.get('amount', '0')
        category = request.POST.get('category')
        expense_date = request.POST.get('date')
        description = request.POST.get('description', '').strip()
        
        # Validation
        if not title:
            messages.error(request, 'Expense title is required!')
            return redirect('manager_app:dashboard')
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messages.error(request, 'Amount must be greater than 0!')
                return redirect('manager_app:dashboard')
        except ValueError:
            messages.error(request, 'Please enter a valid amount!')
            return redirect('manager_app:dashboard')
        
        if not expense_date:
            messages.error(request, 'Date is required!')
            return redirect('manager_app:dashboard')
        
        # Convert date string to date object
        try:
            expense_date = datetime.strptime(expense_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Please enter a valid date!')
            return redirect('manager_app:dashboard')
        
        Expense.objects.create(
            user=request.user,
            title=title,
            amount=amount,
            category=category,
            date=expense_date,
            description=description
        )
        
        messages.success(request, f'Added expense: {title} (${amount:.2f})')
        
    except (OperationalError, ProgrammingError) as e:
        messages.error(request, 'Database tables not found. Please run migrations: python manage.py migrate')
    except Exception as e:
        messages.error(request, f'Error adding expense: {str(e)}')
    
    return redirect('manager_app:dashboard')

def handle_add_event(request):
    """Handle adding new event"""
    try:
        title = request.POST.get('title', '').strip()
        event_date = request.POST.get('date')
        event_time = request.POST.get('time')
        description = request.POST.get('description', '').strip()
        
        # Validation
        if not title:
            messages.error(request, 'Event title is required!')
            return redirect('manager_app:dashboard')
        
        if not event_date:
            messages.error(request, 'Date is required!')
            return redirect('manager_app:dashboard')
        
        # Convert date string to date object
        try:
            event_date = datetime.strptime(event_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Please enter a valid date!')
            return redirect('manager_app:dashboard')
        
        # Convert time string to time object if provided
        event_time_obj = None
        if event_time:
            try:
                event_time_obj = datetime.strptime(event_time, '%H:%M').time()
            except ValueError:
                messages.error(request, 'Please enter a valid time!')
                return redirect('manager_app:dashboard')
        
        Event.objects.create(
            user=request.user,
            title=title,
            date=event_date,
            time=event_time_obj,
            description=description
        )
        
        messages.success(request, f'Added event: {title}')
        
    except (OperationalError, ProgrammingError) as e:
        messages.error(request, 'Database tables not found. Please run migrations: python manage.py migrate')
    except Exception as e:
        messages.error(request, f'Error adding event: {str(e)}')
    
    return redirect('manager_app:dashboard')

def handle_update_budget(request):
    """Handle updating monthly budget"""
    try:
        budget_amount = float(request.POST.get('budget_amount', 0))
        today = date.today()
        
        if budget_amount < 0:
            messages.error(request, 'Budget amount cannot be negative!')
            return redirect('manager_app:dashboard')
        
        # Get or create budget for current month
        budget, created = Budget.objects.get_or_create(
            user=request.user,
            month=today.month,
            year=today.year,
            defaults={'total_budget': budget_amount}
        )
        
        if not created:
            budget.total_budget = budget_amount
            budget.save()
        
        action = 'Set' if created else 'Updated'
        messages.success(request, f'{action} monthly budget to ${budget_amount:.2f}')
        
    except ValueError:
        messages.error(request, 'Please enter a valid budget amount!')
    except (OperationalError, ProgrammingError) as e:
        messages.error(request, 'Database tables not found. Please run migrations: python manage.py migrate')
    except Exception as e:
        messages.error(request, f'Error updating budget: {str(e)}')
    
    return redirect('manager_app:dashboard')

def get_dashboard_context(user):
    """Get all dashboard data with error handling"""
    today = date.today()
    current_month = today.month
    current_year = today.year
    
    # Initialize context with safe defaults
    context = {
        'inventory_items': [],
        'low_stock_items': [],
        'recent_expenses': [],
        'total_expenses_today': 0,
        'weekly_expenses': 0,
        'monthly_expenses': 0,
        'total_budget': 0,
        'remaining_budget': 0,
        'budget_percentage': 0,
        'upcoming_events': [],
        'today_events': [],
        'total_inventory_items': 0,
        'total_inventory_value': 0,
        'low_stock_count': 0,
    }
    
    try:
        # Check if tables exist by making a simple query
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
        
        # Get inventory items with ordering
        try:
            inventory_items = InventoryItem.objects.filter(user=user).order_by('-date_updated')[:10]
            context['inventory_items'] = inventory_items
            
            # Get low stock items (quantity <= 5)
            low_stock_items = InventoryItem.objects.filter(
                user=user, 
                quantity__lte=5
            ).order_by('quantity')
            context['low_stock_items'] = low_stock_items
            
            # Calculate inventory statistics
            total_inventory_items = InventoryItem.objects.filter(user=user).count()
            total_inventory_value = sum(item.quantity for item in inventory_items)
            
            context.update({
                'total_inventory_items': total_inventory_items,
                'total_inventory_value': total_inventory_value,
                'low_stock_count': low_stock_items.count(),
            })
            
        except (OperationalError, ProgrammingError):
            # InventoryItem table doesn't exist
            pass
        
        # Get recent expenses (last 10)
        try:
            recent_expenses = Expense.objects.filter(user=user).order_by('-date')[:10]
            context['recent_expenses'] = recent_expenses
            
            # Get today's expenses
            today_expenses = Expense.objects.filter(user=user, date=today)
            total_expenses_today = today_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
            
            # Get weekly expenses
            week_ago = today - timedelta(days=7)
            weekly_expenses = Expense.objects.filter(
                user=user,
                date__gte=week_ago,
                date__lte=today
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            # Get monthly expenses
            monthly_expenses = Expense.objects.filter(
                user=user, 
                date__month=current_month, 
                date__year=current_year
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            context.update({
                'total_expenses_today': total_expenses_today,
                'weekly_expenses': weekly_expenses,
                'monthly_expenses': monthly_expenses,
            })
            
        except (OperationalError, ProgrammingError):
            # Expense table doesn't exist
            pass
        
        # Get or create budget for current month
        try:
            budget, created = Budget.objects.get_or_create(
                user=user,
                month=current_month,
                year=current_year,
                defaults={'total_budget': 0}
            )
            
            # Calculate remaining budget and budget percentage
            remaining_budget = budget.total_budget - context['monthly_expenses']
            budget_percentage = 0
            if budget.total_budget > 0:
                budget_percentage = (context['monthly_expenses'] / budget.total_budget) * 100
            
            context.update({
                'total_budget': budget.total_budget,
                'remaining_budget': remaining_budget,
                'budget_percentage': min(budget_percentage, 100),  # Cap at 100%
            })
            
        except (OperationalError, ProgrammingError):
            # Budget table doesn't exist
            pass
        
        # Get upcoming events (next 10)
        try:
            upcoming_events = Event.objects.filter(
                user=user, 
                date__gte=today
            ).order_by('date', 'time')[:10]
            
            # Get today's events
            today_events = Event.objects.filter(user=user, date=today).order_by('time')
            
            context.update({
                'upcoming_events': upcoming_events,
                'today_events': today_events,
            })
            
        except (OperationalError, ProgrammingError):
            # Event table doesn't exist
            pass
            
    except (OperationalError, ProgrammingError) as e:
        # Database connection issues or tables don't exist
        pass
    except Exception as e:
        # Any other unexpected errors
        pass
    
    return context

# Additional views for individual pages
@login_required
def inventory_view(request):
    """Inventory page view with search and pagination"""
    try:
        inventory_items = InventoryItem.objects.filter(user=request.user)
        
        # Search functionality
        search_query = request.GET.get('search', '')
        if search_query:
            inventory_items = inventory_items.filter(
                Q(item_name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__icontains=search_query)
            )
        
        # Category filter
        category_filter = request.GET.get('category', '')
        if category_filter:
            inventory_items = inventory_items.filter(category=category_filter)
        
        # Ordering
        inventory_items = inventory_items.order_by('-date_updated')
        
        # Pagination
        paginator = Paginator(inventory_items, 20)  # 20 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Get all categories for filter dropdown
        categories = InventoryItem.objects.filter(user=request.user).values_list(
            'category', flat=True
        ).distinct()
        
        context = {
            'page_obj': page_obj,
            'search_query': search_query,
            'category_filter': category_filter,
            'categories': categories,
            'total_items': inventory_items.count(),
        }
        
    except (OperationalError, ProgrammingError):
        messages.error(request, 'Database tables not found. Please run migrations: python manage.py migrate')
        context = {
            'page_obj': None,
            'search_query': '',
            'category_filter': '',
            'categories': [],
            'total_items': 0,
        }
    
    return render(request, 'manager_app/inventory.html', context)

@login_required
def expenses_view(request):
    """Expenses page view with filtering and pagination"""
    try:
        expenses = Expense.objects.filter(user=request.user)
        
        # Date range filter
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                expenses = expenses.filter(date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                expenses = expenses.filter(date__lte=end_date)
            except ValueError:
                pass
        
        # Category filter
        category_filter = request.GET.get('category', '')
        if category_filter:
            expenses = expenses.filter(category=category_filter)
        
        # Search functionality
        search_query = request.GET.get('search', '')
        if search_query:
            expenses = expenses.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Ordering
        expenses = expenses.order_by('-date', '-date_created')
        
        # Calculate totals
        total_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Pagination
        paginator = Paginator(expenses, 15)  # 15 expenses per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Get all categories for filter dropdown
        categories = Expense.objects.filter(user=request.user).values_list(
            'category', flat=True
        ).distinct()
        
        context = {
            'page_obj': page_obj,
            'search_query': search_query,
            'category_filter': category_filter,
            'start_date': start_date,
            'end_date': end_date,
            'categories': categories,
            'total_amount': total_amount,
            'total_expenses': expenses.count(),
        }
        
    except (OperationalError, ProgrammingError):
        messages.error(request, 'Database tables not found. Please run migrations: python manage.py migrate')
        context = {
            'page_obj': None,
            'search_query': '',
            'category_filter': '',
            'start_date': None,
            'end_date': None,
            'categories': [],
            'total_amount': 0,
            'total_expenses': 0,
        }
    
    return render(request, 'manager_app/expenses.html', context)

@login_required
def calendar_view(request):
    """Calendar page view with month navigation"""
    # Get month and year from URL parameters
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    today = date.today()
    
    if month and year:
        try:
            current_month = int(month)
            current_year = int(year)
        except ValueError:
            current_month = today.month
            current_year = today.year
    else:
        current_month = today.month
        current_year = today.year
    
    try:
        # Get events for the selected month
        events = Event.objects.filter(
            user=request.user,
            date__month=current_month,
            date__year=current_year
        ).order_by('date', 'time')
        
        # Get all events for the user (for navigation)
        all_events = Event.objects.filter(user=request.user).order_by('date')
        
        context = {
            'events': events,
            'all_events': all_events,
            'current_month': current_month,
            'current_year': current_year,
            'today': today,
        }
        
    except (OperationalError, ProgrammingError):
        messages.error(request, 'Database tables not found. Please run migrations: python manage.py migrate')
        context = {
            'events': [],
            'all_events': [],
            'current_month': current_month,
            'current_year': current_year,
            'today': today,
        }
    
    return render(request, 'manager_app/calendar.html', context)

@login_required
def budget_view(request):
    """Budget page view with monthly budget management"""
    # Handle budget creation/update
    if request.method == 'POST':
        return handle_budget_form(request)
    
    today = date.today()
    
    try:
        budgets = Budget.objects.filter(user=request.user).order_by('-year', '-month')
        
        # Get current month expenses grouped by category
        current_month_expenses = Expense.objects.filter(
            user=request.user,
            date__month=today.month,
            date__year=today.year
        )
        
        monthly_expenses_total = current_month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Group expenses by category for current month
        expense_by_category = {}
        for expense in current_month_expenses:
            category = expense.category or 'Other'
            if category in expense_by_category:
                expense_by_category[category] += expense.amount
            else:
                expense_by_category[category] = expense.amount
        
        # Get current month budget
        current_budget = Budget.objects.filter(
            user=request.user,
            month=today.month,
            year=today.year
        ).first()
        
        context = {
            'budgets': budgets,
            'monthly_expenses': monthly_expenses_total,
            'expense_by_category': expense_by_category,
            'current_budget': current_budget,
            'current_month': today.month,
            'current_year': today.year,
        }
        
    except (OperationalError, ProgrammingError):
        messages.error(request, 'Database tables not found. Please run migrations: python manage.py migrate')
        context = {
            'budgets': [],
            'monthly_expenses': 0,
            'expense_by_category': {},
            'current_budget': None,
            'current_month': today.month,
            'current_year': today.year,
        }
    
    return render(request, 'manager_app/budget.html', context)

def handle_budget_form(request):
    """Handle budget form submission"""
    try:
        budget_amount = float(request.POST.get('budget_amount', 0))
        month = int(request.POST.get('month', date.today().month))
        year = int(request.POST.get('year', date.today().year))
        
        if budget_amount < 0:
            messages.error(request, 'Budget amount cannot be negative!')
            return redirect('budget')
        
        # Get or create budget
        budget, created = Budget.objects.get_or_create(
            user=request.user,
            month=month,
            year=year,
            defaults={'total_budget': budget_amount}
        )
        
        if not created:
            budget.total_budget = budget_amount
            budget.save()
        
        action = 'Created' if created else 'Updated'
        messages.success(request, f'{action} budget for {month}/{year}: ${budget_amount:.2f}')
        
    except (ValueError, TypeError):
        messages.error(request, 'Please enter valid budget details!')
    except (OperationalError, ProgrammingError):
        messages.error(request, 'Database tables not found. Please run migrations: python manage.py migrate')
    except Exception as e:
        messages.error(request, f'Error managing budget: {str(e)}')
    
    return redirect('budget')

# AJAX views for dynamic updates
@login_required
def delete_inventory_item(request, item_id):
    """Delete inventory item via AJAX"""
    if request.method == 'POST':
        try:
            item = get_object_or_404(InventoryItem, id=item_id, user=request.user)
            item_name = item.item_name
            item.delete()
            return JsonResponse({
                'success': True, 
                'message': f'Deleted {item_name} from inventory'
            })
        except (OperationalError, ProgrammingError):
            return JsonResponse({
                'success': False, 
                'message': 'Database tables not found. Please run migrations: python manage.py migrate'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error deleting item: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def delete_expense(request, expense_id):
    """Delete expense via AJAX"""
    if request.method == 'POST':
        try:
            expense = get_object_or_404(Expense, id=expense_id, user=request.user)
            expense_title = expense.title
            expense.delete()
            return JsonResponse({
                'success': True, 
                'message': f'Deleted expense: {expense_title}'
            })
        except (OperationalError, ProgrammingError):
            return JsonResponse({
                'success': False, 
                'message': 'Database tables not found. Please run migrations: python manage.py migrate'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error deleting expense: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def delete_event(request, event_id):
    """Delete event via AJAX"""
    if request.method == 'POST':
        try:
            event = get_object_or_404(Event, id=event_id, user=request.user)
            event_title = event.title
            event.delete()
            return JsonResponse({
                'success': True, 
                'message': f'Deleted event: {event_title}'
            })
        except (OperationalError, ProgrammingError):
            return JsonResponse({
                'success': False, 
                'message': 'Database tables not found. Please run migrations: python manage.py migrate'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error deleting event: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def profile_view(request):
    """Display user profile page"""
    context = {
        'user': request.user,
        # Add any additional context data you need
    }
    return render(request, 'manager_app/profile.html', context)