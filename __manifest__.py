{
    "name" : "Project Cost Estimate Module",
    "description" : "A custom module integrates project module with cost estimation features.",
    "version" : "18.0.1.0.0",
    "author" : "Mohamed Elbanna",
    "data" : [
        "security/ir.model.access.csv",
        "views/project_cost_estimate_views.xml",
        "views/root_menu.xml",
    ],
    "depends" : ["base", "project" , "mail"],
    "assets" : {
        "web.assets_backend" : [],
        "web.assets_qweb" : [],
    },
    "application" : True,
}