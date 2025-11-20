{
    "name" : "Project Cost Estimate Module",
    "description" : "A custom module integrates project module with cost estimation features.",
    "version" : "18.0.1.0.0",
    "author" : "Mohamed Elbanna",
    "data" : [
        "security/project_cost_estimate_security.xml",
        "security/ir.model.access.csv",
        "data/mail_template.xml",
        "views/project_cost_estimate_views.xml",
        "views/project_project_inherited_views.xml",
        "views/root_menu.xml",
    ],
    "depends" : ["base", "project" , "mail"],
    "assets" : {
        "web.assets_backend" : [
            "project_cost_estimate/static/src/css/project_cost_estimate.css",
        ],
        "web.assets_qweb" : [],
    },
    "application" : True,
}