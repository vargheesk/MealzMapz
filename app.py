
from dateutil.parser import parse
import os
from datetime import datetime
from functools import wraps
from math import radians, cos, sin, asin, sqrt
from flask import Flask, render_template, request, redirect, url_for, flash,  session
from flask_mail import Mail, Message
from supabase import create_client, Client

from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

# decrtor for login
def login_required(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


   



def calculate_distance(lat1, lon1, lat2, lon2):
    
    
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    
    # haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # radus 
    r = 6371
    distance = c * r
    
    
    print(f"Distance calculation: ({lat1*180/3.14159:.6f}, {lon1*180/3.14159:.6f}) to ({lat2*180/3.14159:.6f}, {lon2*180/3.14159:.6f}) = {distance:.2f} km")
    
    return distance













# gollobalizing the loction
def get_user_location():
    
    try:
        if 'user_lat' in session and 'user_lon' in session:
            lat = float(session['user_lat'])
            lon = float(session['user_lon'])
            print(f"Retrieved user location from session: {lat}, {lon}")
            return lat, lon
        else:
            print("No user location found in session")
            return None, None
    except (ValueError, TypeError) as e:
        print(f"Error parsing user location from session: {e}")
        return None, None






















    

def notify_followers_about_new_post(user_id, post_title, user_name):
    try:

        #select s.subscriber_id, u.email, u.name from subscriptions s join users u on s.subscriber_id = u.id where s.followed_user_id = '-user_id-';
        followers_data = supabase.table('subscriptions').select('subscriber_id, users!subscriptions_subscriber_id_fkey(email, name)').eq('followed_user_id', user_id).execute()
        
        if followers_data.data:
            subject = f"New Food Available from {user_name} - MealMap"
            
            for follower in followers_data.data:
                if follower.get('users') and follower['users'].get('email'):
                    follower_email = follower['users']['email']
                    follower_name = follower['users']['name']
                    
                    body = f"""Hello {follower_name},

                        {user_name} has just posted new surplus food on MealMap:

                        "{post_title}"

                        Visit MealMap now to view the details and claim this food before it expires.

                        Best regards,
                        The MealMap Team"""
                    
                    

                    msg = Message(subject=subject, recipients=[follower_email], body=body)
                    mail.send(msg)


        return True
    except Exception as e:
        print(f"\nError sending follower notifications: {e}\n\n")
        return False


















def delete_expired_listings():
    """
    Delete all expired listings from Supabase.
    Expired = expiry_time exists and is in the past.
    """
    try:
        now = datetime.now(timezone.utc).isoformat()

        # delete from listings where expiry_time < '-now-';
        response = supabase.table("listings").delete().lt("expiry_time", now).execute()
        print(response)

    except Exception as e:
        print(f"Error deleting expired listings: {e}")
        return {"deleted_count": 0, "error": str(e)}























#==============================================================================================================================================================================================================
# -----------------------------------------------------------------------------------------------     Routes starting    -----------------------------------------------------------------------------------
#=============================================================================================================================================================================================================



@app.route('/')
def index():
    return render_template('index.html')











@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        
        try:
            # authaicte with supabase
            auth_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if auth_response.user:
                # eamil verictn check
                if not getattr(auth_response.user, 'email_confirmed', True):
                    flash('Please verify your email before logging in. Check your inbox for the verification link.', 'warning')
                    supabase.auth.sign_out()
                    return render_template('auth/login.html')
                
                # Get user profile from database
                #select * from users where id = 'user_id';
                user_data = supabase.table('users').select('*').eq('id', auth_response.user.id).execute()
                
                if user_data.data:
                    user = user_data.data[0]
                    session['user_id'] = str(user['id'])
                    session['user_name'] = user['name']
                    session['user_email'] = user['email']
                    session['user_role'] = user['role']
                    
                    flash(f'Welcome back, {user["name"]}!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('User profile not found. Please contact support.', 'error')
                    supabase.auth.sign_out()
            else:
                flash('Invalid email or password.', 'error')
                
        except Exception as e:
            error_message = str(e)
            print(f"Login error: {e}")
            if 'Invalid login credentials' in error_message:
                flash('Invalid email or password.', 'error')
            elif 'Email not confirmed' in error_message:
                flash('Please verify your email before logging in. Check your inbox for the verification link.', 'warning')


    return render_template('auth/login.html')




















@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        organisation_type = request.form.get('organisation_type') if role == 'organisation' else None
        organisation_description = request.form.get('organisation_description') if role == 'organisation' else None
        
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('auth/signup.html')
        
        try:
            # sending eamil verfictin
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "name": name,
                        "role": role
                    }
                }
            })
            
            if auth_response.user:
                
                user_profile = {
                    'id': auth_response.user.id,
                    'name': name,
                    'email': email,
                    'role': role,
                    'organisation_type': organisation_type,
                    'organisation_description': organisation_description,
                    'created_at': datetime.utcnow().isoformat()
                }
                
                profile_response = supabase.table('users').insert(user_profile).execute()
                
                if profile_response.data:
                    flash(f'Account created successfully! Please check your email ({email}) and click the verification link before logging in.', 'success')
                    return redirect(url_for('login'))
                else:
                    flash('Failed to create user profile. Please try again.', 'error')
            else:
                flash('Failed to create account. Please try again.', 'error')
                
        except Exception as e:
            error_message = str(e)
            print(f"Signup error: {e}")
            flash(error_message, 'error')
    
    return render_template('auth/signup.html')





















@app.route('/logout')
def logout():
    try:
        supabase.auth.sign_out()
    except:
        pass
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


















@app.route('/profile')
@login_required
def profile():
    
    try:

        user_posts = supabase.table('listings').select('*').eq('user_id', session['user_id']).eq('category', 'Food').order('created_at', desc=True).execute()
        user_places = supabase.table('listings').select('*').eq('user_id', session['user_id']).eq('category', 'Place').order('created_at', desc=True).execute()
        user_data = supabase.table('users').select('*').eq('id', session['user_id']).execute()


        user = user_data.data[0] if user_data.data else None
        
        # converting to proper time
        if user and user.get('created_at'):
            user['created_at'] = parse(user['created_at'])
        
        for post in user_posts.data:
            if post.get('created_at'):
                post['created_at'] = parse(post['created_at'])
            if post.get('expiry_time'):
                post['expiry_time'] = parse(post['expiry_time'])
        
        for place in user_places.data:
            if place.get('created_at'):
                place['created_at'] = parse(place['created_at'])
        
        return render_template('auth/profile.html', user=user, user_posts=user_posts.data, user_places=user_places.data)
    
    except Exception as e:
        print(f"Profile error: {e}")
        flash('Error loading profile.', 'error')
        return redirect(url_for('index'))
    














@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    
    try:
        user_data = supabase.table('users').select('*').eq('id', session['user_id']).execute()
        user = user_data.data[0] if user_data.data else None
        
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('profile'))
        
        if request.method == 'POST':
            name = request.form.get('name')
            organisation_type = request.form.get('organisation_type') if user['role'] == 'organisation' else None
            organisation_description = request.form.get('organisation_description') if user['role'] == 'organisation' else None
            
            if not name:
                flash('Name is required.', 'error')
                return render_template('auth/edit_profile.html', user=user)
            
            
            update_data = {
                'name': name,
                'organisation_type': organisation_type,
                'organisation_description': organisation_description,
                'updated_at': datetime.utcnow().isoformat()
            }
            
            response = supabase.table('users').update(update_data).eq('id', session['user_id']).execute()
            
            if response.data:
                session['user_name'] = name
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Failed to update profile. Please try again.', 'error')
        
        return render_template('auth/edit_profile.html', user=user)
    except Exception as e:
        print(f"Edit profile error: {e}")
        flash('Error updating profile.', 'error')
        return redirect(url_for('profile'))
























@app.route('/map')
def map_view():
    """Map view with location-based filtering"""
    try:
        
        user_lat = request.args.get('lat')
        user_lon = request.args.get('lon')
        radius = request.args.get('radius', 5.0) 
        
        
        if not user_lat or not user_lon:
            user_lat, user_lon = get_user_location()
        
        # Convert to float and set default radius
        try:
            radius = float(radius)
            if radius <= 0:
                radius = 5.0
        except (ValueError, TypeError):
            radius = 5.0
        
        listings_data = []
        
        # If user location is available, filter by radius
        if user_lat and user_lon:
            try:
                user_lat = float(user_lat)
                user_lon = float(user_lon)
                
                # Get all active listings from database
                all_listings_response = supabase.table('listings').select('*, users!listings_user_id_fkey(name, role, organisation_type)').execute()
                all_listings = all_listings_response.data or []
                
                # Filter listings within radius
                for listing in all_listings:
                    try:
                        # Skip listings without valid coordinates
                        if not listing.get('lat') or not listing.get('lon'):
                            continue
                        
                        listing_lat = float(listing['lat'])
                        listing_lon = float(listing['lon'])
                        
                        # Calculate distance
                        distance = calculate_distance(user_lat, user_lon, listing_lat, listing_lon)
                        
                        # Include if within radius
                        if distance <= radius:
                            # Prepare listing data for map
                            listing_data = {
                                'id': listing['id'],
                                'title': listing.get('title', ''),
                                'description': listing.get('description', ''),
                                'category': listing.get('category', ''),
                                'cost_type': listing.get('cost_type', ''),
                                'lat': listing_lat,
                                'lon': listing_lon,
                                'image_url': listing.get('image_url', ''),
                                'distance': round(distance, 2),
                                'expiry_time': listing.get('expiry_time'),
                                'timings': listing.get('timings'),
                                'user_name': listing.get('users', {}).get('name', 'Unknown'),
                                'user_role': listing.get('users', {}).get('role', 'individual')
                            }
                            listings_data.append(listing_data)
                    
                    except (ValueError, TypeError) as e:
                        print(f"Error processing listing {listing.get('id')}: {e}")
                        continue
                
                # Sort by distance
                listings_data.sort(key=lambda x: x['distance'])
                
                print(f"Found {len(listings_data)} listings within {radius}km of user location")
                
            except (ValueError, TypeError) as e:
                print(f"Error processing user location: {e}")
                user_lat = user_lon = None
        
        return render_template('map.html', 
                             listings=listings_data, 
                             user_lat=user_lat, 
                             user_lon=user_lon, 
                             radius=radius,
                             has_location=bool(user_lat and user_lon))
        
    except Exception as e:
        print(f"Map error: {e}")
        return render_template('map.html', 
                             listings=[], 
                             user_lat=None, 
                             user_lon=None, 
                             radius=5.0,
                             has_location=False)















@app.route('/posts')
def posts():
    """Food posts and places listing with filters"""
    try:
        delete_expired_listings()

        all_listings = supabase.table('listings').select('*').order('created_at', desc=True).execute()

        category_filter = request.args.get('category', 'all')
        cost_filter = request.args.get('cost_type', 'all')
        sort_by = request.args.get('sort', 'recent')
        
        listings = all_listings.data

        if category_filter != 'all':
            listings = [l for l in listings if l['category'] == category_filter]
        
        if cost_filter != 'all':
            listings = [l for l in listings if l['cost_type'] == cost_filter]
        
        user_lat, user_lon = get_user_location()
        
        if sort_by == 'distance' and user_lat and user_lon:
            listings.sort(key=lambda x: x.get('distance', float('inf')))
        elif sort_by == 'expiry':
            listings = [l for l in listings if l.get('expiry_time')]
            listings.sort(key=lambda x: x['expiry_time'])
        
        return render_template('posts.html', listings=listings)
    except Exception as e:
        print(f"Posts error: {e}")
        return render_template('posts.html', listings=[])
















@app.route('/post/<int:post_id>')
def post_details(post_id):
    """View detailed post/place information with follow functionality"""
    try:
        # Get post details with user information
        post_data = supabase.table('listings').select('*, users!listings_user_id_fkey(name, role, organisation_type, organisation_description)').eq('id', post_id).execute()
        
        print("\n\n")
        print(post_data.data)
        print("\n\n")
        if not post_data.data:
            flash('Post not found.', 'error')
            return redirect(url_for('posts'))
        
        post = post_data.data[0]
        
        # Check if current user is following the post author
        is_following = False
        if 'user_id' in session:
            follow_check = supabase.table('subscriptions').select('id').eq('subscriber_id', session['user_id']).eq('followed_user_id', post['user_id']).execute()
            is_following = len(follow_check.data) > 0
        
        # Calculate distance if user location is available
        user_lat, user_lon = get_user_location()
        if user_lat and user_lon:
            post['distance'] = calculate_distance(user_lat, user_lon, float(post['lat']), float(post['lon']))
        

        print("\n\n")
        print(post)
        print("\n\n")
        print(post_data.data)
        print("\n\n")
        return render_template('post_details.html', post=post, is_following=is_following, session=session)
    except Exception as e:
        print(f"Post details error: {e}")
        flash('Error loading post details.', 'error')
        return redirect(url_for('posts'))
















@app.route('/follow/<user_id>', methods=['POST'])
@login_required
def follow_user(user_id):
    try:
        
        
        existing_follow = supabase.table('subscriptions').select('id').eq('subscriber_id', session['user_id']).eq('followed_user_id', user_id).execute()
        
        if existing_follow.data:
            supabase.table('subscriptions').delete().eq('subscriber_id', session['user_id']).eq('followed_user_id', user_id).execute()
            flash('Successfully unfollowed user.', 'success')
        else:
            new_subscription = {
                'subscriber_id': session['user_id'],
                'followed_user_id': user_id,
                'created_at': datetime.utcnow().isoformat()
            }
            response = supabase.table('subscriptions').insert(new_subscription).execute()
            if response.data:
                flash('Successfully following user.', 'success')
            else:
                flash('Failed to follow user.', 'error')
        
        return redirect(request.referrer or url_for('posts'))
    except Exception as e:
        print(f"Follow user error: {e}")
        flash('Error processing follow request.', 'error')
        return redirect(request.referrer or url_for('posts'))
















# Separate routes for surplus food and community places
@app.route('/add_surplus_food', methods=['GET', 'POST'])
@login_required
def add_surplus_food():
    """Add surplus food post"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        lat = float(request.form.get('lat'))
        lon = float(request.form.get('lon'))
        cost_type = request.form.get('cost_type')
        image_url = request.form.get('image_url')
        expiry_datetime = request.form.get('expiry_datetime')
        
        # Validation
        if not all([title, description, lat, lon, cost_type, expiry_datetime]):
            flash('Please fill in all required fields.', 'error')
            return render_template('add_surplus_food.html')
        
        try:
            expiry_time = datetime.fromisoformat(expiry_datetime.replace('T', ' '))
            
            new_listing = {
                'user_id': session['user_id'],
                'category': 'Food',
                'cost_type': cost_type,
                'title': title,
                'description': description,
                'lat': lat,
                'lon': lon,
                'image_url': image_url if image_url else None,
                'expiry_time': expiry_time.isoformat(),
                'timings': None  # Not used for food posts
            }
            
            response = supabase.table('listings').insert(new_listing).execute()

            if response.data:
                notify_followers_about_new_post(session['user_id'], title, session['user_name'])
                flash('Food post added successfully!', 'success')
                return redirect(url_for('posts'))
            else:
                flash('Failed to add food post. Please try again.', 'error')
        except Exception as e:
            print(f"Add surplus food error: {e}")
            flash('Error adding food post. Please try again.', 'error')
    
    return render_template('add_surplus_food.html')














@app.route('/add_community_place', methods=['GET', 'POST'])
@login_required
def add_community_place():
    """Add community place"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        lat = float(request.form.get('lat'))
        lon = float(request.form.get('lon'))
        cost_type = request.form.get('cost_type')
        timings = request.form.get('timings')
        image_url = request.form.get('image_url')
        
        # Validation
        if not all([title, description, lat, lon, cost_type, timings]):
            flash('Please fill in all required fields.', 'error')
            return render_template('add_community.html')
        
        try:
            new_listing = {
                'user_id': session['user_id'],
                'category': 'Place',
                'cost_type': cost_type,
                'title': title,
                'description': description,
                'lat': lat,
                'lon': lon,
                'image_url': image_url if image_url else None,
                'expiry_time': None,  # Not used for places
                'timings': timings
            }
            
            response = supabase.table('listings').insert(new_listing).execute()
            
            if response.data:
                flash('Community place added successfully!', 'success')
                return redirect(url_for('posts'))
            else:
                flash('Failed to add community place. Please try again.', 'error')
        except Exception as e:
            print(f"Add community place error: {e}")
            flash('Error adding community place. Please try again.', 'error')
    
    return render_template('add_community.html')

@app.route('/edit_food_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_food_post(post_id):
    """Edit food post"""
    try:
        post_data = supabase.table('listings').select('*').eq('id', post_id).eq('user_id', session['user_id']).eq('category', 'Food').execute()
        print(post_data)
        if not post_data.data:
            flash('Food post not found or you do not have permission to edit it.', 'error')
            return redirect(url_for('profile'))
        
        post = post_data.data[0]
        
        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            cost_type = request.form.get('cost_type')
            image_url = request.form.get('image_url')
            expiry_datetime = request.form.get('expiry_datetime')
            

            if image_url:  
                
                if not image_url.startswith(('http://', 'https://')):
                    image_url = None
            else:
                
                image_url = None


            if not all([title, description, cost_type, expiry_datetime]):
                flash('Please fill in all required fields.', 'error')
                return render_template('edit_food_post.html', post=post)
            
            expiry_time = datetime.fromisoformat(expiry_datetime.replace('T', ' '))
            
            update_data = {
                'title': title,
                'description': description,
                'cost_type': cost_type,
                'image_url': image_url if image_url else None,
                'expiry_time': expiry_time.isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            response = supabase.table('listings').update(update_data).eq('id', post_id).execute()
            
            if response.data:
                flash('Food post updated successfully!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Failed to update food post. Please try again.', 'error')
        
        return render_template('edit_food_post.html', post=post)
    except Exception as e:
        print(f"Edit food post error: {e}")
        flash('Error editing food post.', 'error')
        return redirect(url_for('profile'))




@app.route('/edit_community_place/<int:place_id>', methods=['GET', 'POST'])
@login_required
def edit_community_place(place_id):
    """Edit community place"""
    try:
        place_data = supabase.table('listings').select('*').eq('id', place_id).eq('user_id', session['user_id']).eq('category', 'Place').execute()
        
        if not place_data.data:
            flash('Community place not found or you do not have permission to edit it.', 'error')
            return redirect(url_for('profile'))
        
        place = place_data.data[0]



        # print("\n",place,"\n") #-------------------------------------------------------------------------------------------------------
        



        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')            
            cost_type = request.form.get('cost_type')
            timings = request.form.get('timings')
            image_url = request.form.get('image_url')
            
            if not all([title, description,cost_type, timings]):
                flash('Please fill in all required fields.', 'error')
                return render_template('edit_community_place.html', place=place,place_id=place_id)
            
            update_data = {
                'title': title,
                'description': description,
                'cost_type': cost_type,
                'timings': timings,
                'image_url': image_url if image_url else None,
                'updated_at': datetime.utcnow().isoformat()
            }
            
            response = supabase.table('listings').update(update_data).eq('id', place_id).execute()
            
            if response.data:
                flash('Community place updated successfully!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Failed to update community place. Please try again.', 'error')
        
        return render_template('edit_community_place.html', place=place,place_id=place_id)
    except Exception as e:
        print(f"Edit community place error: {e}")
        flash('Error editing community place.', 'error')
        return redirect(url_for('profile'))






@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete post or place"""
    try:
        # Verify ownership
        post_data = supabase.table('listings').select('*').eq('id', post_id).eq('user_id', session['user_id']).execute()
        
        if not post_data.data:
            flash('Post not found or you do not have permission to delete it.', 'error')
            return redirect(url_for('profile'))
        
        # Delete the post
        response = supabase.table('listings').delete().eq('id', post_id).execute()
        
        if response.data:
            flash('Post deleted successfully!', 'success')
        else:
            flash('Failed to delete post. Please try again.', 'error')
    except Exception as e:
        print(f"Delete post error: {e}")
        flash('Error deleting post.', 'error')
    
    return redirect(url_for('profile'))













# Legacy route for backward compatibility
@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    """Legacy add post route - redirects to surplus food"""
    return redirect(url_for('add_surplus_food'))

@app.route('/set_location', methods=['POST'])
def set_location():
    """Set user location in session"""
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    
    if lat and lon:
        session['user_lat'] = float(lat)
        session['user_lon'] = float(lon)
        flash('Location updated successfully!', 'success')
    else:
        flash('Failed to update location.', 'error')
    
    return redirect(request.referrer or url_for('index'))













@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500







if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)