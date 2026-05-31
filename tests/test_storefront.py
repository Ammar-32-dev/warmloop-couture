import re
import pytest
from playwright.sync_api import Page, expect

# Enforce django_db on all tests in this file
pytestmark = pytest.mark.django_db(transaction=True)

def test_homepage_rendering(live_server, page: Page):
    """
    Test Case 1: Product catalog rendering, banner, tickers, and seed garments.
    """
    # Navigate to live server
    page.goto(live_server.url)
    
    # 1. Assert title is correct
    expect(page).to_have_title("WARMLOOP // COUTURE Storefront")
    
    # 2. Assert luxury header exists
    expect(page.locator("text=WARMLOOP // COUTURE").first).to_be_visible()
    
    # 3. Assert promo banner exists
    expect(page.locator("text=THE COUTURE")).to_be_visible()
    expect(page.locator("text=RUNWAY REVELATION")).to_be_visible()
    expect(page.locator("text=Enter the Runway")).to_be_visible()
    
    # 4. Assert kinetic ticker exists
    expect(page.locator(".ticker-wrap")).to_be_visible()
    expect(page.locator("text=NEW COUTURE DROP")).to_be_visible()
    
    # 5. Verify product listing contains seeded items
    expect(page.locator("text=CURATED COUTURE")).to_be_visible()
    expect(page.locator("text=Handwoven Banarasi Silk Saree")).to_be_visible()
    expect(page.locator("text=Lucknowi Chikankari Georgette Kurta")).to_be_visible()
    expect(page.locator("text=Obsidian Heavyweight Graphic Hoodie")).to_be_visible()


def test_theme_toggle(live_server, page: Page):
    """
    Test Case 2: Zero-Glitch Theme toggle and LocalStorage preservation.
    """
    page.goto(live_server.url)
    
    # Verify default theme (Light mode, no dark class)
    expect(page.locator("html")).not_to_have_class("dark")
    
    # Locate toggle button
    theme_btn = page.locator("#theme-toggle")
    expect(theme_btn).to_be_visible()
    
    # Toggle theme to Dark
    theme_btn.click()
    expect(page.locator("html")).to_have_class("dark")
    
    # Reload page to assert local storage persistence
    page.reload()
    expect(page.locator("html")).to_have_class("dark")
    
    # Toggle back to Light
    theme_btn.click()
    expect(page.locator("html")).not_to_have_class("dark")


def test_product_detail_view(live_server, page: Page):
    """
    Test Case 3: Transition to product detail view and specification grid.
    """
    page.goto(live_server.url)
    
    # Click details link of the hoodie
    hoodie_link = page.locator("text=Obsidian Heavyweight Graphic Hoodie")
    expect(hoodie_link).to_be_visible()
    hoodie_link.click()
    
    # Assert navigation to product detail screen
    expect(page).to_have_title("WARMLOOP // Obsidian Heavyweight Graphic Hoodie")
    expect(page.locator("text=Garment Narrative")).to_be_visible()
    
    # Verify specification grid values
    expect(page.locator("span", has_text="400 GSM French Terry").first).to_be_visible()
    expect(page.locator("span", has_text="Avant-Garde Oversized").first).to_be_visible()


def test_purchase_cart_workflow(live_server, page: Page):
    """
    Test Case 4: End-to-End cart lifecycle (Add, Update Quantity, Remove).
    """
    page.goto(live_server.url)
    
    # 1. Assert Cart is initially empty
    cart_link = page.locator("a:has-text('Cart')")
    expect(cart_link).to_be_visible()
    cart_link.click()
    
    expect(page.locator("text=Your couture cart is currently empty.")).to_be_visible()
    
    # 2. Return to runway, open product detail, and add to cart
    page.locator("text=Explore Runway").click()
    page.locator("text=Handwoven Banarasi Silk Saree").click()
    
    # Submit add-to-cart form from product detail screen
    page.locator("button:has-text('Add to Cart')").click()
    
    # Assert successful redirection to cart page containing the item
    expect(page.locator("text=Your Runway Selections")).to_be_visible()
    expect(page.locator("text=Handwoven Banarasi Silk Saree")).to_be_visible()
    expect(page.locator("text=Subtotal: ₹8499.00")).to_be_visible()
    
    # 3. Assert summary is correctly updated
    summary_card = page.locator("text=Summary")
    expect(summary_card).to_be_visible()
    expect(page.locator("text=Total Items").locator("..").locator("span").nth(1)).to_have_text("1")
    expect(page.locator("text=Total Value").locator("..").locator("span").nth(1)).to_have_text("₹8499.00")
    
    # 4. Update quantity in cart to 2
    qty_input = page.locator("input[name='quantity']")
    qty_input.fill("2")
    # Submit quantity form by pressing Enter, avoiding any pointer overlaps with the absolute positioned Remove button
    qty_input.press("Enter")
    
    # Assert price recalculations
    expect(page.locator("text=Subtotal: ₹16998.00")).to_be_visible()
    expect(page.locator("text=Total Items").locator("..").locator("span").nth(1)).to_have_text("2")
    expect(page.locator("text=Total Value").locator("..").locator("span").nth(1)).to_have_text("₹16998.00")
    
    # 5. Remove item from cart and verify empty state
    page.locator("button:has-text('Remove')").click()
    expect(page.locator("text=Your couture cart is currently empty.")).to_be_visible()


def test_category_dropdown_filtering(live_server, page: Page):
    """
    Test Case 5: Verify category filtering via Collections dropdown and visual resets.
    """
    page.goto(live_server.url)
    
    # Verify Collections navigation item is present
    collections_btn = page.locator("button:has-text('Collections')").first
    expect(collections_btn).to_be_visible()
    
    # Hover to reveal Collections list
    collections_btn.hover()
    
    # Select category "Modern Streetwear"
    streetwear_link = page.locator("a:has-text('Modern Streetwear')").first
    expect(streetwear_link).to_be_visible()
    streetwear_link.click()
    
    # Verify exact URL pattern and layout changes
    expect(page).to_have_url(f"{live_server.url}/?category=modern-streetwear#store-grid")
    expect(page.locator("text=CURATED // MODERN STREETWEAR")).to_be_visible()
    expect(page.locator("text=THE MODERN STREETWEAR")).to_be_visible()
    expect(page.locator("span.gradient-text", has_text="COLLECTION").first).to_be_visible()
    
    # Verify that only Streetwear items are shown (Saree from Ethnic Wear must be filtered out)
    expect(page.locator("text=Obsidian Heavyweight Graphic Hoodie")).to_be_visible()
    expect(page.locator("text=Handwoven Banarasi Silk Saree")).not_to_be_visible()
    
    # Reset filter back to runway catalog
    page.locator("text=View Full Runway").click()
    
    # Verify both products are visible again
    expect(page.locator("text=Handwoven Banarasi Silk Saree")).to_be_visible()
    expect(page.locator("text=Obsidian Heavyweight Graphic Hoodie")).to_be_visible()


def test_bespoke_atelier_modal_flow(live_server, page: Page):
    """
    Test Case 6: Verify Bespoke Atelier Modal flow, interactive inputs, and Success card confirmation.
    """
    page.goto(live_server.url)
    
    # Bespoke menu trigger button check
    bespoke_btn = page.locator("button[onclick='openBespokeModal()']").first
    expect(bespoke_btn).to_be_visible()
    
    # Modal starts closed
    modal = page.locator("#bespoke-modal")
    expect(modal).not_to_have_class(re.compile("opacity-100"))
    
    # Open modal
    bespoke_btn.click()
    expect(modal).to_have_class(re.compile("opacity-100"))
    
    # Fill in luxury inquiry
    page.locator("#bespoke-name").fill("Devendra C.")
    page.locator("#bespoke-email").fill("devendra@warmloop.com")
    page.locator("#bespoke-discipline").select_option("streetwear")
    page.locator("#bespoke-details").fill("Looking for a customized heavyweight cyber hoodie adjusted to 500 GSM and double zip system.")
    
    # Submit request
    page.locator("button:has-text('Request Atelier Curation')").click()
    
    # Verify success confirmation card
    expect(page.locator("#bespoke-success-message")).to_be_visible()
    expect(page.locator("text=Request Received")).to_be_visible()
    expect(page.locator("#success-client-name")).to_have_text("Devendra C.")
    expect(page.locator("#success-client-email")).to_have_text("devendra@warmloop.com")
    
    # Dismiss success modal and return to runway
    page.locator("button:has-text('Return to Runway')").click()
    expect(modal).not_to_have_class(re.compile("opacity-100"))


def test_user_authentication_lifecycle(live_server, page: Page):
    """
    Test Case 7: Verify registration, custom dynamic header menu changes, logout, and login.
    """
    page.goto(live_server.url)
    
    # 1. Open guest menu and click Register
    page.locator("#user-menu-btn").click()
    expect(page.locator("text=Guest Mode")).to_be_visible()
    
    signup_link = page.locator("a:has-text('Register / Sign Up')")
    expect(signup_link).to_be_visible()
    signup_link.click()
    
    # 2. Assert signup page loaded
    expect(page).to_have_title("Sign Up // WARMLOOP COUTURE")
    expect(page.locator("text=Create an account to save custom sizes")).to_be_visible()
    
    # 3. Register a new user
    page.locator("input[name='username']").fill("couture_shopper")
    page.locator("input[name='password1']").fill("Couture123!")
    page.locator("input[name='password2']").fill("Couture123!")
    
    page.locator("button:has-text('Register Membership')").click()
    
    # 4. Redirection to runway catalog on success
    expect(page).to_have_title("WARMLOOP // COUTURE Storefront")
    
    # 5. Profile trigger should display first letter "C"
    profile_btn = page.locator("#user-menu-btn")
    expect(profile_btn).to_be_visible()
    expect(profile_btn).to_contain_text("C")
    
    # 6. Click profile trigger to open dropdown and log out
    profile_btn.click()
    expect(page.locator("text=Atelier Profile")).to_be_visible()
    expect(page.locator("text=couture_shopper")).to_be_visible()
    
    # Log out
    page.locator("a:has-text('Log Out')").click()
    expect(page).to_have_title("WARMLOOP // COUTURE Storefront")
    
    # 7. Re-open guest menu to check logout state, then click Log In
    page.locator("#user-menu-btn").click()
    expect(page.locator("text=Guest Mode")).to_be_visible()
    
    login_link = page.locator("a:has-text('Log In')")
    expect(login_link).to_be_visible()
    login_link.click()
    
    # 8. Assert login page loaded
    expect(page).to_have_title("Log In // WARMLOOP COUTURE")
    
    # Log back in
    page.locator("input[name='username']").fill("couture_shopper")
    page.locator("input[name='password']").fill("Couture123!")
    
    page.locator("button:has-text('Log In Profile')").click()
    
    # 9. Verify successful log in state in header
    expect(page).to_have_title("WARMLOOP // COUTURE Storefront")
    expect(page.locator("#user-menu-btn")).to_contain_text("C")


def test_mobile_navigation_menu_flow(live_server, page: Page):
    """
    Test Case 8: Verify mobile menu toggle, drawer layout, and interaction on narrow viewports.
    """
    page.goto(live_server.url)
    
    # 1. Set viewport to mobile size (iPhone)
    page.set_viewport_size({"width": 390, "height": 844})
    
    # 2. Desktop navbar links should be hidden
    expect(page.locator("nav.md\\:flex")).to_be_hidden()
    
    # 3. Mobile menu button is visible
    mobile_btn = page.locator("button[title='Toggle Navigation Menu']")
    expect(mobile_btn).to_be_visible()
    
    # 4. Mobile menu starts hidden
    mobile_menu = page.locator("#mobile-menu")
    expect(mobile_menu).not_to_have_class(re.compile("opacity-100"))
    
    # 5. Open mobile menu
    mobile_btn.click()
    expect(mobile_menu).to_have_class(re.compile("opacity-100"))
    
    # 6. Verify mobile menu links exist
    expect(mobile_menu.locator("a:has-text('Runway')").first).to_be_visible()
    expect(mobile_menu.locator("span", has_text="Collections").first).to_be_visible()
    expect(mobile_menu.locator("a:has-text('Modern Streetwear')").first).to_be_visible()
    
    # 7. Clicking Bespoke Atelier in mobile menu closes it and opens Bespoke Modal
    mobile_menu.locator("button:has-text('Bespoke Atelier')").click()
    
    # Confirm mobile menu closes and Bespoke modal launches
    expect(mobile_menu).not_to_have_class(re.compile("opacity-100"))
    
    bespoke_modal = page.locator("#bespoke-modal")
    expect(bespoke_modal).to_have_class(re.compile("opacity-100"))
    
    # 8. Close Bespoke Modal
    bespoke_modal.locator("button[title='Close Consultation Modal']").click()
    expect(bespoke_modal).not_to_have_class(re.compile("opacity-100"))




