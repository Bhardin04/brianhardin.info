import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestDarkModeImplementation:
    """Test dark mode implementation in templates."""

    def test_homepage_has_dark_mode_classes(self):
        """Test that homepage includes dark mode classes."""
        response = client.get("/")
        assert response.status_code == 200
        content = response.text
        
        # Check that body has dark mode classes
        assert 'class="bg-gray-50 dark:bg-gray-900' in content
        assert 'class="bg-white dark:bg-gray-800' in content
        
        # Check that main heading has dark mode classes
        assert 'text-gray-900 dark:text-white' in content
        
        # Check that technology cards have dark mode classes
        assert 'bg-white dark:bg-gray-800' in content
        
        # Check that dark mode toggle button exists
        assert 'id="theme-toggle"' in content
        assert 'theme-toggle-dark-icon' in content
        assert 'theme-toggle-light-icon' in content

    def test_contact_page_has_dark_mode_classes(self):
        """Test that contact page includes dark mode classes."""
        response = client.get("/contact")
        assert response.status_code == 200
        content = response.text
        
        # Check that main heading has dark mode classes
        assert 'text-gray-900 dark:text-white' in content
        
        # Check that subheading has dark mode classes
        assert 'text-gray-600 dark:text-gray-300' in content

    def test_blog_page_has_dark_mode_classes(self):
        """Test that blog page includes dark mode classes."""
        response = client.get("/blog")
        assert response.status_code == 200
        content = response.text
        
        # Check that page includes dark mode classes
        assert 'dark:' in content
        assert 'dark:bg-gray-900' in content

    def test_projects_page_has_dark_mode_classes(self):
        """Test that projects page includes dark mode classes."""
        response = client.get("/projects")
        assert response.status_code == 200
        content = response.text
        
        # Check that page includes dark mode classes
        assert 'dark:' in content
        assert 'dark:bg-gray-900' in content

    def test_dark_mode_toggle_script_included(self):
        """Test that dark mode toggle script is included in all pages."""
        pages = ["/", "/about", "/contact", "/projects", "/blog"]
        
        for page in pages:
            response = client.get(page)
            assert response.status_code == 200
            content = response.text
            
            # Check that dark mode script is included
            assert 'theme-toggle' in content
            assert 'localStorage.getItem(' in content
            assert 'classList.add(' in content

    def test_dark_mode_tailwind_config(self):
        """Test that Tailwind is configured for dark mode."""
        response = client.get("/")
        assert response.status_code == 200
        content = response.text
        
        # Check that Tailwind is configured with dark mode
        assert "darkMode: 'class'" in content

    def test_navigation_has_dark_mode_classes(self):
        """Test that navigation elements have dark mode classes."""
        response = client.get("/")
        assert response.status_code == 200
        content = response.text
        
        # Check navigation dark mode classes
        assert 'bg-white dark:bg-gray-800' in content
        assert 'dark:text-gray-300 dark:hover:text-white' in content

    def test_footer_has_dark_mode_classes(self):
        """Test that footer has dark mode classes."""
        response = client.get("/")
        assert response.status_code == 200
        content = response.text
        
        # Check footer dark mode classes
        assert 'bg-gray-800 dark:bg-gray-900' in content

    def test_dark_mode_icons_present(self):
        """Test that both light and dark mode icons are present."""
        response = client.get("/")
        assert response.status_code == 200
        content = response.text
        
        # Check that both icons are present
        assert 'theme-toggle-dark-icon' in content
        assert 'theme-toggle-light-icon' in content
        
        # Check that icons have proper SVG paths
        assert 'M17.293 13.293A8 8 0 016.707 2.707' in content  # Moon icon
        assert 'M10 2L13.09 8.26L20 9L14' in content  # Sun icon

    def test_dark_mode_color_transitions(self):
        """Test that color transitions are included."""
        response = client.get("/")
        assert response.status_code == 200
        content = response.text
        
        # Check that transitions are included
        assert 'transition-colors' in content
        assert 'duration-200' in content


class TestDarkModeAccessibility:
    """Test dark mode accessibility features."""

    def test_dark_mode_button_has_proper_attributes(self):
        """Test that dark mode toggle button has accessibility attributes."""
        response = client.get("/")
        assert response.status_code == 200
        content = response.text
        
        # Check button accessibility
        assert 'type="button"' in content
        assert 'focus:outline-none' in content
        assert 'focus:ring-4' in content

    def test_dark_mode_contrast_classes(self):
        """Test that dark mode uses proper contrast classes."""
        response = client.get("/")
        assert response.status_code == 200
        content = response.text
        
        # Check contrast in dark mode
        assert 'dark:text-white' in content  # High contrast white text
        assert 'dark:text-gray-300' in content  # Medium contrast gray text
        assert 'dark:text-gray-400' in content  # Lower contrast gray text
        assert 'dark:bg-gray-900' in content  # Dark background
        assert 'dark:bg-gray-800' in content  # Slightly lighter dark background