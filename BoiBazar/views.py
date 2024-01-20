from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from book.models import Book


def index(request):
    books = Book.objects.all()
    fiction_books = Book.objects.filter(category='Fiction')
    non_fiction_books = Book.objects.filter(category='Non-Fiction')
    mystery_books = Book.objects.filter(category='Mystery')
    thriller_books = Book.objects.filter(category='Thriller')
    novels = Book.objects.filter(category='Novels')
    comics = Book.objects.filter(category='Comics')
    biography = Book.objects.filter(category='Biography')
    horror = Book.objects.filter(category='Horror')
    others = Book.objects.filter(category='Others')
    
    context = {
        'books': books,
        'fiction_books': fiction_books,
        'non_fiction_books': non_fiction_books,
        'mystery_books': mystery_books,
        'thriller_books': thriller_books,
        'novels': novels,
        'comics': comics,
        'biography': biography,
        'horror': horror,
        'others': others,

    }

    return render(request, 'index.html', context)

def cart(request):
    if request.method == "POST":
        # Get the product ID and quantity from the submitted form
        book_id = request.POST.get("proid")
        quantity = 1 # Default value
        # Retrieve the cart from the session
        cart = request.session.get('cart', {})
        cart[book_id] = cart.get(book_id, 0) + quantity
        # Update the cart in the session
        request.session['cart'] = cart
        return redirect('cart')

    cart = request.session.get('cart', {})  # Retrieve the cart dictionary from the session

    # store book information and quantity
    cart_data = []

    total_price = 0

    for book_id, quantity in cart.items():
        book = Book.get_detail(id=book_id)
        if book:
            item_price = book.book_price * quantity
            total_price += item_price
            cart_data.append({
                'book': book,
                'quantity': quantity,
                'item_price': item_price,
            })

    email = request.session.get('email')
    
    context = {
        'cart_data': cart_data,
        'total_price': total_price,
        'email': email,
    }

    return render(request, 'cart.html', context)
def remove_from_cart(request):
    if request.method == "POST":
        book_id = request.POST.get("proid")
        
        cart = request.session.get('cart', {})
        if book_id in cart:
            # Remove the selected product from the cart
            del cart[book_id]
            request.session['cart'] = cart
    return redirect('cart')

def borrow_book(request, book_id):
    # Retrieve the book based on the book_id
    book = Book.objects.get(id=book_id)
    if book.is_available:
        book.is_available = False
        book.save()
        return JsonResponse({'message': 'Book borrowed successfully.'})
    else:
        return JsonResponse({'message': 'Book is not available for borrowing.'})

def navbar(request):
    return render(request, 'navbar.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')