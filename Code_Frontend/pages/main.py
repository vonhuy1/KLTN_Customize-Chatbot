import os
from streamlit_navigation_bar import st_navbar
import pages.page1 as pg
pages = ["Home","Settings","Profile", "Guide", "Contacts", "About Us"]
parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(parent_dir, "123.svg")
styles = {
    "nav": {
        "background": "linear-gradient(to right, #c8d9ff 20%, #4fc9de 60%, #54248e 100%) !important;",
        "justify-content": "center",
        "font-weight":"bold",
        "font-family": 'fangsong',
        "font-size": "18px"
    },
    "img": {
        "padding-right": "14px",
        "width": "60px",
        "height": "60px"

    },
    "span": {
        "color": "black",
        "padding": "15px",
    },
    "active": {
        "color": "var(--text-color)",
        "background-color": "rgb(84 230 175 / 83%)",
        "font-weight": "bold",
        "padding": "14px",
    }
}
options = {
    "show_menu": True,
    "show_sidebar": True,
    "hide_nav": False
}

page = st_navbar(
    pages,
    logo_path=logo_path,
    styles=styles,
    options= options,
    adjust=True
    )

functions = {
    "Home": pg.show_home,
    "Profile": pg.show_profile,
    "Settings": pg.show_settings,
    "Guide": pg.show_user_guide,
    "Contacts": pg.show_contacts,
    "About Us": pg.show_about,
}

if __name__ == '__main__':
    go_to = functions.get(page)
    if go_to:
       go_to()