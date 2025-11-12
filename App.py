import streamlit as st
import pandas as pd
import json
from datetime import datetime
import io

# Page config
st.set_page_config(
    page_title="Philly Me Up - Menu Manager",
    page_icon="🥙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #374151;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #f59e0b;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background-color: #f59e0b;
        color: white;
        font-weight: 600;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #d97706;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'menu_items' not in st.session_state:
    st.session_state.menu_items = []
    st.session_state.initialized = False

def initialize_menu_data():
    """Initialize the menu with all Philly Me Up items"""
    menu_items = [
        # Starters
        {"name": "Egg Rolls (2pcs)", "category": "Starters", "price": 5.00, "description": "Crispy egg rolls filled with seasoned vegetables and served with sweet chili sauce", "sku": "PHI-EGG-001", "stock": "instock"},
        {"name": "Loaded Fries", "category": "Starters", "price": 8.00, "description": "Crispy fries topped with melted cheese, bacon bits, sour cream, and chives", "sku": "PHI-FRI-001", "stock": "instock"},
        {"name": "Buffalo Shrimp", "category": "Starters", "price": 10.00, "description": "Jumbo shrimp tossed in spicy buffalo sauce, served with ranch dressing", "sku": "PHI-SHR-001", "stock": "instock"},
        {"name": "Mozzarella Sticks (6pcs)", "category": "Starters", "price": 7.00, "description": "Golden-fried mozzarella sticks served with marinara sauce", "sku": "PHI-MOZ-001", "stock": "instock"},
        {"name": "Onion Rings", "category": "Starters", "price": 6.00, "description": "Thick-cut onion rings, perfectly breaded and fried to golden perfection", "sku": "PHI-ONI-001", "stock": "instock"},
        {"name": "Chicken Tenders (4pcs)", "category": "Starters", "price": 9.00, "description": "Crispy chicken tenders served with honey mustard or BBQ sauce", "sku": "PHI-CHK-001", "stock": "instock"},
        {"name": "Philly Spring Rolls (3pcs)", "category": "Starters", "price": 8.00, "description": "Crispy spring rolls filled with cheesesteak ingredients", "sku": "PHI-SPR-001", "stock": "instock"},
        {"name": "Loaded Nachos", "category": "Starters", "price": 11.00, "description": "Tortilla chips loaded with cheese, jalapeños, sour cream, salsa, and guacamole", "sku": "PHI-NAC-001", "stock": "instock"},
        {"name": "Fried Pickles", "category": "Starters", "price": 6.50, "description": "Tangy dill pickle spears, breaded and fried, served with ranch", "sku": "PHI-PIC-001", "stock": "instock"},
        {"name": "Mac & Cheese Bites (6pcs)", "category": "Starters", "price": 7.50, "description": "Creamy mac and cheese breaded and fried to perfection", "sku": "PHI-MAC-001", "stock": "instock"},
        {"name": "Pretzel Bites with Cheese", "category": "Starters", "price": 7.00, "description": "Soft pretzel bites served with warm cheese dip", "sku": "PHI-PRE-001", "stock": "instock"},
        
        # Salads
        {"name": "Caesar Salad", "category": "Salads", "price": 8.00, "description": "Fresh romaine lettuce, parmesan cheese, croutons, and Caesar dressing", "sku": "PHI-SAL-001", "stock": "instock", "addons": "protein"},
        {"name": "House Garden Salad", "category": "Salads", "price": 7.00, "description": "Mixed greens, tomatoes, cucumbers, red onions, and choice of dressing", "sku": "PHI-SAL-002", "stock": "instock", "addons": "protein"},
        {"name": "Buffalo Chicken Salad", "category": "Salads", "price": 12.00, "description": "Mixed greens topped with crispy buffalo chicken, tomatoes, cucumbers, and ranch dressing", "sku": "PHI-SAL-003", "stock": "instock"},
        
        # Cheesesteaks & Entrees
        {"name": "Classic Philly Cheesesteak", "category": "Cheesesteaks", "price": 12.00, "description": "Thinly sliced ribeye steak, grilled onions, and melted cheese on a hoagie roll", "sku": "PHI-CHE-001", "stock": "instock", "addons": "cheesesteak"},
        {"name": "Chicken Cheesesteak", "category": "Cheesesteaks", "price": 11.00, "description": "Grilled chicken breast, sautéed onions, and melted cheese on a hoagie roll", "sku": "PHI-CHE-002", "stock": "instock", "addons": "cheesesteak"},
        {"name": "Pizza Steak", "category": "Cheesesteaks", "price": 13.00, "description": "Cheesesteak topped with marinara sauce and mozzarella cheese", "sku": "PHI-CHE-003", "stock": "instock", "addons": "cheesesteak"},
        {"name": "BBQ Bacon Cheesesteak", "category": "Cheesesteaks", "price": 14.00, "description": "Steak with BBQ sauce, crispy bacon, and cheddar cheese", "sku": "PHI-CHE-004", "stock": "instock", "addons": "cheesesteak"},
        {"name": "Buffalo Chicken Cheesesteak", "category": "Cheesesteaks", "price": 12.50, "description": "Spicy buffalo chicken with ranch dressing and melted cheese", "sku": "PHI-CHE-005", "stock": "instock", "addons": "cheesesteak"},
        
        # Pasta
        {"name": "Chicken Alfredo Pasta", "category": "Pasta", "price": 14.00, "description": "Fettuccine pasta with grilled chicken in creamy Alfredo sauce", "sku": "PHI-PAS-001", "stock": "instock"},
        {"name": "Shrimp Scampi Pasta", "category": "Pasta", "price": 16.00, "description": "Linguine with garlic butter shrimp, white wine sauce, and parsley", "sku": "PHI-PAS-002", "stock": "instock"},
        {"name": "Philly Cheesesteak Pasta", "category": "Pasta", "price": 15.00, "description": "Penne pasta with cheesesteak meat, peppers, onions, and cheese sauce", "sku": "PHI-PAS-003", "stock": "instock"},
        {"name": "Cajun Chicken Pasta", "category": "Pasta", "price": 14.50, "description": "Penne with blackened chicken, peppers, onions, and Cajun cream sauce", "sku": "PHI-PAS-004", "stock": "instock"},
        
        # Wings
        {"name": "Classic Buffalo Wings (6pc)", "category": "Wings", "price": 10.00, "description": "Traditional buffalo wings with celery and ranch or blue cheese", "sku": "PHI-WIN-001", "stock": "instock"},
        {"name": "BBQ Wings (6pc)", "category": "Wings", "price": 10.00, "description": "Wings tossed in tangy BBQ sauce", "sku": "PHI-WIN-002", "stock": "instock"},
        {"name": "Honey Garlic Wings (6pc)", "category": "Wings", "price": 10.00, "description": "Sweet and savory honey garlic glazed wings", "sku": "PHI-WIN-003", "stock": "instock"},
        {"name": "Lemon Pepper Wings (6pc)", "category": "Wings", "price": 10.00, "description": "Crispy wings seasoned with zesty lemon pepper", "sku": "PHI-WIN-004", "stock": "instock"},
        
        # Dips
        {"name": "Ranch Dip", "category": "Dips", "price": 1.50, "description": "Creamy ranch dipping sauce", "sku": "PHI-DIP-001", "stock": "instock"},
        {"name": "Cheese Sauce", "category": "Dips", "price": 2.00, "description": "Warm cheese dipping sauce", "sku": "PHI-DIP-002", "stock": "instock"},
    ]
    
    st.session_state.menu_items = menu_items
    st.session_state.initialized = True

def generate_woocommerce_csv():
    """Generate WooCommerce CSV with WP Cafe features"""
    items = st.session_state.menu_items
    
    csv_data = []
    for item in items:
        row = {
            'ID': '',
            'Type': 'simple',
            'SKU': item['sku'],
            'Name': item['name'],
            'Published': '1',
            'Is featured?': '1' if item['category'] in ['Cheesesteaks', 'Pasta'] else '0',
            'Visibility in catalog': 'visible',
            'Short description': item['description'][:100],
            'Description': item['description'],
            'Date sale price starts': '',
            'Date sale price ends': '',
            'Tax status': 'taxable',
            'Tax class': '',
            'In stock?': '1',
            'Stock': '',
            'Low stock amount': '',
            'Backorders allowed?': '0',
            'Sold individually?': '0',
            'Weight (lbs)': '',
            'Length (in)': '',
            'Width (in)': '',
            'Height (in)': '',
            'Allow customer reviews?': '1',
            'Purchase note': '',
            'Sale price': '',
            'Regular price': f"{item['price']:.2f}",
            'Categories': f"Menu, {item['category']}",
            'Tags': f"{item['category']}, Philly Food, Restaurant",
            'Shipping class': '',
            'Images': '',
            'Download limit': '',
            'Download expiry days': '',
            'Parent': '',
            'Grouped products': '',
            'Upsells': '',
            'Cross-sells': '',
            'External URL': '',
            'Button text': '',
            'Position': '0',
        }
        
        # Add WP Cafe specific fields
        if item.get('addons') == 'protein':
            row['Meta: reserv_extra_fields'] = json.dumps([{
                "type": "radio",
                "label": "Add Protein",
                "required": False,
                "options": [
                    {"label": "None", "price": "0"},
                    {"label": "Grilled Chicken", "price": "3.00"},
                    {"label": "Steak", "price": "4.00"},
                    {"label": "Salmon", "price": "5.00"}
                ]
            }])
        elif item.get('addons') == 'cheesesteak':
            row['Meta: reserv_extra_fields'] = json.dumps([
                {
                    "type": "radio",
                    "label": "Choose Your Cheese",
                    "required": True,
                    "options": [
                        {"label": "American", "price": "0"},
                        {"label": "Provolone", "price": "0"},
                        {"label": "Cheese Whiz", "price": "0"}
                    ]
                },
                {
                    "type": "checkbox",
                    "label": "Extras",
                    "required": False,
                    "options": [
                        {"label": "Extra Cheese", "price": "1.50"},
                        {"label": "Mushrooms", "price": "1.00"},
                        {"label": "Hot Peppers", "price": "0.50"},
                        {"label": "Sweet Peppers", "price": "0.50"}
                    ]
                }
            ])
        else:
            row['Meta: reserv_extra_fields'] = ''
        
        row['Meta: preparation_time'] = '15-20 minutes'
        row['Meta: _stock_status'] = item['stock']
        
        csv_data.append(row)
    
    df = pd.DataFrame(csv_data)
    return df

# Main App
st.markdown('<div class="main-header">🥙 Philly Me Up - Menu Manager</div>', unsafe_allow_html=True)

# Initialize data if needed
if not st.session_state.initialized:
    initialize_menu_data()

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Select Page", ["Dashboard", "Menu Items", "Add New Item", "Export CSV"])
    
    st.markdown("---")
    st.subheader("Quick Stats")
    total_items = len(st.session_state.menu_items)
    categories = len(set(item['category'] for item in st.session_state.menu_items))
    avg_price = sum(item['price'] for item in st.session_state.menu_items) / total_items if total_items > 0 else 0
    
    st.metric("Total Items", total_items)
    st.metric("Categories", categories)
    st.metric("Avg Price", f"${avg_price:.2f}")

# Dashboard Page
if page == "Dashboard":
    st.markdown('<div class="section-header">Dashboard Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        starters = len([i for i in st.session_state.menu_items if i['category'] == 'Starters'])
        st.markdown(f"""
            <div class="metric-card">
                <h3>{starters}</h3>
                <p>Starters</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        salads = len([i for i in st.session_state.menu_items if i['category'] == 'Salads'])
        st.markdown(f"""
            <div class="metric-card">
                <h3>{salads}</h3>
                <p>Salads</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        cheesesteaks = len([i for i in st.session_state.menu_items if i['category'] == 'Cheesesteaks'])
        st.markdown(f"""
            <div class="metric-card">
                <h3>{cheesesteaks}</h3>
                <p>Cheesesteaks</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        pasta = len([i for i in st.session_state.menu_items if i['category'] == 'Pasta'])
        st.markdown(f"""
            <div class="metric-card">
                <h3>{pasta}</h3>
                <p>Pasta</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Price Distribution by Category</div>', unsafe_allow_html=True)
    
    # Create price chart
    df = pd.DataFrame(st.session_state.menu_items)
    chart_data = df.groupby('category')['price'].agg(['mean', 'min', 'max']).reset_index()
    
    st.bar_chart(chart_data.set_index('category')['mean'])
    
    st.markdown('<div class="section-header">Recent Menu Items</div>', unsafe_allow_html=True)
    recent_items = st.session_state.menu_items[:5]
    for item in recent_items:
        with st.expander(f"{item['name']} - ${item['price']:.2f}"):
            st.write(f"**Category:** {item['category']}")
            st.write(f"**SKU:** {item['sku']}")
            st.write(f"**Description:** {item['description']}")
            if item.get('addons'):
                st.write(f"**Add-ons Available:** Yes ({item['addons']})")

# Menu Items Page
elif page == "Menu Items":
    st.markdown('<div class="section-header">All Menu Items</div>', unsafe_allow_html=True)
    
    # Filter options
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("Search items", placeholder="Search by name or SKU...")
    with col2:
        category_filter = st.selectbox("Filter by Category", ["All"] + sorted(set(item['category'] for item in st.session_state.menu_items)))
    
    # Filter items
    filtered_items = st.session_state.menu_items
    if search:
        filtered_items = [i for i in filtered_items if search.lower() in i['name'].lower() or search.lower() in i['sku'].lower()]
    if category_filter != "All":
        filtered_items = [i for i in filtered_items if i['category'] == category_filter]
    
    # Display items
    for idx, item in enumerate(filtered_items):
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.write(f"**{item['name']}**")
            st.caption(item['description'][:80] + "...")
        with col2:
            st.write(f"${item['price']:.2f}")
        with col3:
            st.write(item['category'])
        with col4:
            if st.button("Edit", key=f"edit_{idx}"):
                st.session_state.editing_item = idx
                st.rerun()
        
        st.markdown("---")

# Add New Item Page
elif page == "Add New Item":
    st.markdown('<div class="section-header">Add New Menu Item</div>', unsafe_allow_html=True)
    
    with st.form("add_item_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Item Name*")
            category = st.selectbox("Category*", ["Starters", "Salads", "Cheesesteaks", "Pasta", "Wings", "Dips", "Desserts", "Beverages"])
            price = st.number_input("Price ($)*", min_value=0.0, step=0.50, format="%.2f")
        
        with col2:
            sku = st.text_input("SKU*", placeholder="PHI-XXX-001")
            stock = st.selectbox("Stock Status", ["instock", "outofstock", "onbackorder"])
            addons = st.selectbox("Add-ons", ["none", "protein", "cheesesteak"])
        
        description = st.text_area("Description*", placeholder="Enter a detailed description of the menu item...")
        
        submitted = st.form_submit_button("Add Item")
        
        if submitted:
            if name and category and price and sku and description:
                new_item = {
                    "name": name,
                    "category": category,
                    "price": price,
                    "description": description,
                    "sku": sku,
                    "stock": stock,
                }
                if addons != "none":
                    new_item["addons"] = addons
                
                st.session_state.menu_items.append(new_item)
                st.success(f"Successfully added {name} to the menu!")
                st.balloons()
            else:
                st.error("Please fill in all required fields marked with *")

# Export CSV Page
elif page == "Export CSV":
    st.markdown('<div class="section-header">Export Menu to CSV</div>', unsafe_allow_html=True)
    
    st.write("Generate a WooCommerce-compatible CSV file with WP Cafe features for your Philly Me Up menu.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"📊 Total items to export: **{len(st.session_state.menu_items)}**")
    with col2:
        st.info(f"📁 File format: **WooCommerce CSV**")
    
    st.markdown("### Preview")
    df_preview = pd.DataFrame(st.session_state.menu_items)
    st.dataframe(df_preview, use_container_width=True)
    
    if st.button("Generate CSV", type="primary"):
        with st.spinner("Generating CSV file..."):
            csv_df = generate_woocommerce_csv()
            
            # Convert to CSV
            csv_buffer = io.StringIO()
            csv_df.to_csv(csv_buffer, index=False)
            csv_string = csv_buffer.getvalue()
            
            st.success("CSV file generated successfully!")
            
            # Download button
            st.download_button(
                label="Download CSV",
                data=csv_string,
                file_name=f"philly-me-up-menu-{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
            
            st.markdown("### CSV Preview")
            st.dataframe(csv_df.head(10), use_container_width=True)
