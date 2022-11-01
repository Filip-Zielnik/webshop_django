from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import AddAddressForm, AddCommentForm, ChangePasswordForm, LoginForm, ProfileForm, UpdateProfileForm, \
    UpdateUserForm, UserForm
from .models import Address, Cart, Comment, Product, Profile, Order


class HomeView(View):
    """ Displays homepage. """

    def get(self, request):
        """ Home view. """
        return render(request=request, template_name="home.html")


class RegistrationView(View):
    """ Allows user to create account. """

    def get(self, request):
        """ Displays registration form with extended django-user's fields. """
        user_form = UserForm
        profile_form = ProfileForm
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request=request, template_name="registration.html", context=context)

    def post(self, request):
        """ Creates a new user. """
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            birth_date = profile_form.cleaned_data['birth_date']
            user = user_form.save()
            profile = Profile.objects.create(user=user, birth_date=birth_date)
            profile.save()
            user.set_password(user.password)
            user.save()
        else:
            messages.error(request, 'Nie udało się założyć konta!')
            context = {
                'user_form': user_form,
                'profile_form': profile_form,
            }
            return render(request=request, template_name="registration.html", context=context)
        return render(request=request, template_name="registration_message.html")


class UpdateUserView(LoginRequiredMixin, View):
    """ Allows user to update specific user's data. """

    login_url = '/login/'

    def get(self, request):
        """ Displays user's data. """
        update_user_form = UpdateUserForm(instance=request.user)
        update_profile_form = UpdateProfileForm(instance=request.user.profile)
        context = {
            'update_user_form': update_user_form,
            'update_profile_form': update_profile_form,
        }
        return render(request=request, template_name="update_user.html", context=context)

    def post(self, request):
        """ Modifies user's data. """
        update_user_form = UpdateUserForm(request.POST, instance=request.user)
        update_profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)

        if update_user_form.is_valid() and update_profile_form.is_valid():
            update_user_form.save()
            update_profile_form.save()
            messages.success(request, 'Dane zostały zmienione!')
        else:
            messages.error(request, 'Dane nie zostały zmienione!')

        context = {
            'update_user_form': update_user_form,
            'update_profile_form': update_profile_form,
        }
        return render(request=request, template_name="update_user.html", context=context)


class ChangePasswordView(LoginRequiredMixin, View):
    """ Allows user to change password. """

    login_url = '/login/'

    def get(self, request):
        """ Displays change password form. """
        form = ChangePasswordForm(instance=request.user)
        context = {
            'form': form,
        }
        return render(request=request, template_name="change_password.html", context=context)

    def post(self, request):
        """ Changes the user's password. """
        form = ChangePasswordForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Hasło zostało zmienione!')
        else:
            messages.error(request, 'Hasło nie zostało zmienione!')

        context = {
            'form': form,
        }
        return render(request=request, template_name="change_password.html", context=context)


class LoginView(View):
    """ Allows user to log in using username & password. """

    def get(self, request):
        """ Displays login form. """
        form = LoginForm
        context = {
            'form': form,
        }
        return render(request=request, template_name="login.html", context=context)

    def post(self, request):
        """ Logs the user in. """
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Niepoprawny login lub hasło!')

        context = {
            'form': form,
        }
        return render(request=request, template_name='login.html', context=context)


class LogoutView(View):
    """ Allows user to log out. """

    def get(self, request):
        """ Logs out the user. """
        logout(request)
        return render(request=request, template_name='logout.html')


class LoggedView(LoginRequiredMixin, View):
    """ User's account view. """

    login_url = '/login/'

    def get(self, request):
        """ Displays user's data such as username, first name, address, ect. """
        address_form = Address.objects.filter(profile_id=request.user.id).order_by('name')
        order_form = Order.objects.filter(user_id=request.user.id).order_by('-order_date')
        context = {
            'address_form': address_form,
            'order_form': order_form,
        }
        return render(request=request, template_name="logged.html", context=context)


class AddressView(LoginRequiredMixin, View):
    """ Allows user to check the address details and to remove it if necessary. """

    login_url = '/login/'

    def get(self, request, address_id):
        """ Displays detailed information about address such as country, city, ect. """
        form = Address.objects.filter(profile_id=request.user.id, id=address_id)
        context = {
            'form': form,
        }
        return render(request=request, template_name="address.html", context=context)

    def post(self, request, address_id):
        """ Deletes the user's address. """
        address = Address.objects.filter(profile_id=request.user.id, id=address_id)
        address.delete()
        return redirect('logged')


class AddAddressView(LoginRequiredMixin, View):
    """ Allows user to add new address. """

    login_url = '/login/'

    def get(self, request):
        """ Displays address form to fill. """
        form = AddAddressForm()
        context = {
            'form': form,
        }
        return render(request=request, template_name="add_address.html", context=context)

    def post(self, request):
        """ Creates new user's address. """
        form = AddAddressForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            address = form.cleaned_data['address']
            zip_code = form.cleaned_data['zip_code']
            address_model = Address.objects.create(
                name=name,
                country=country,
                city=city,
                address=address,
                zip_code=zip_code,
                profile_id=request.user.id,
            )
            address_model.save()
            messages.success(request, 'Adres został dodany!')
        else:
            messages.error(request, 'Adres nie został dodany!')

        context = {
            'form': form,
        }
        return render(request=request, template_name="add_address.html", context=context)


class ChangeAddressView(LoginRequiredMixin, View):
    """ Allows user to change address details. """

    login_url = '/login/'

    def get(self, request, address_id):
        """ Displays changeable address details. """
        address = Address.objects.get(profile_id=request.user.id, id=address_id)
        form = AddAddressForm(instance=address)
        context = {
            'form': form,
        }
        return render(request=request, template_name="change_address.html", context=context)

    def post(self, request, address_id):
        """ Modifies user's address. """
        address = Address.objects.get(profile_id=request.user.id, id=address_id)
        form = AddAddressForm(request.POST, instance=address)

        if form.is_valid():
            form.save()
            messages.success(request, 'Adres został zmieniony!')
        else:
            messages.error(request, 'Adres nie został zmieniony!')

        context = {
            'form': form,
        }
        return render(request=request, template_name="change_address.html", context=context)


class CartView(LoginRequiredMixin, View):
    """ Allows user to check the cart, remove products and to place the order. """

    login_url = '/login/'

    def get(self, request):
        """ Displays products in the cart. """
        form = Cart.objects.filter(user_id=request.user)
        context = {
            'form': form,
        }
        return render(request=request, template_name="cart.html", context=context)

    def post(self, request):
        """ Creates order. NOT FINISHED"""
        user = request.user.id
        order = Order.objects.create(
            user_id=user,
        )
        order.save()
        return render(request=request, template_name="order_placed.html")


@login_required
def add_to_cart(request, pk):
    """ Adds product to the cart. """
    user = request.user.id
    product = get_object_or_404(Product, pk=pk)
    Cart.objects.create(
        product=product,
        user_id=user,
    )
    messages.success(request, 'Dodano produkt do koszyka!')
    return redirect('product', pk=pk)


@login_required
def remove_from_cart(request, cart_id):
    """ Removes product from the cart. """
    cart = Cart.objects.get(user=request.user.id, id=cart_id)
    cart.delete()
    messages.success(request, 'Produkt został usunięty z koszyka!')
    return redirect('cart')


class OrderView(LoginRequiredMixin, View):
    """ Order details view.. """

    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        """ Displays order details. """
        order_form = Order.objects.filter(user_id=request.user.id)
        cart_form = Cart.objects.filter(user=request.user.id)
        context = {
            'order_form': order_form,
            'cart_form': cart_form,
        }
        return render(request=request, template_name="order.html", context=context)


class CpuView(View):
    """ CPUs view. """

    def get(self, request):
        """ Displays only products in CPU category(id=1). """
        form = Product.objects.filter(category_id='1')
        context = {
            'form': form,
        }
        return render(request=request, template_name="category.html", context=context)


class GpuView(View):
    """ GPUs view. """

    def get(self, request):
        """ Displays only products in GPU category(id=2). """
        form = Product.objects.filter(category_id='2')
        context = {
            'form': form,
        }
        return render(request=request, template_name="category.html", context=context)


class MotherboardView(View):
    """ Motherboards view. """

    def get(self, request):
        """ Displays only products in Motherboards category(id=3). """
        form = Product.objects.filter(category_id='3')
        context = {
            'form': form,
        }
        return render(request=request, template_name="category.html", context=context)


class ProductView(View):
    """ Product's details view. """

    def get(self, request, pk):
        """ Displays product details and comments section. """
        product_form = Product.objects.filter(id=pk)
        comment_form = Comment.objects.filter(product_id=pk).order_by('-text_date')
        add_comment_form = AddCommentForm
        context = {
            'product_form': product_form,
            'comment_form': comment_form,
            'add_comment_form': add_comment_form,
        }
        return render(request=request, template_name="product.html", context=context)

    def post(self, request, pk):
        """ Creates comment. """
        add_comment_form = AddCommentForm(data=request.POST)
        if add_comment_form.is_valid():
            text = add_comment_form.cleaned_data['text']
            comment = Comment.objects.create(
                user_id=request.user.id,
                product_id=pk,
                text=text,
            )
            comment.save()
        return redirect('product', pk=pk)


@login_required
def remove_comment(request, comment_id, pk):
    """ Removes comment from product's view. """
    comment = Comment.objects.get(user=request.user.id, id=comment_id)
    comment.delete()
    messages.success(request, 'Komentarz został usunięty!')
    return redirect('product', pk=pk)
