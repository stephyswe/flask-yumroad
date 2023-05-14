from flask_assets import Bundle

common_css = Bundle(
    "https://stackpath.bootstrapcdn.com/bootswatch/4.3.1/litera/bootstrap.min.css",
    "css/common.css",
    filters="cssmin",
    output="public/css/common.css",
)

common_js = Bundle(
    "js/common.js", filters="jsmin", output="public/js/common.js"
)

purchase_js = Bundle(
    "js/purchase.js", filters="jsmin", output="public/js/purchase.js"
)

landing_css = Bundle(
    "https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    "css/landing.css",
    filters="cssmin",
    output="public/css/landing.css",
)
