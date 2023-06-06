graph [
  directed 1
  node [
    id 0
    label "Review_project_portfolio_balance_for_2020_Q1"
  ]
  node [
    id 1
    label "Portfolio_management"
  ]
  node [
    id 2
    label "Conduct_project_assurance_readiness_for_Brexit_Programme"
  ]
  node [
    id 3
    label "P3M_Assessment"
  ]
  node [
    id 4
    label "Identify_best_practice_regulatory_project_as_examplar"
  ]
  node [
    id 5
    label "P3M_Support"
  ]
  node [
    id 6
    label "Cross-project_review_of_plastic_dependencies"
  ]
  node [
    id 7
    label "P3M_Optimisation"
  ]
  node [
    id 8
    label "Rescope_large_project_which_has_failed_to_deliver_in_2020"
  ]
  node [
    id 9
    label "Project_Programme_recovery"
  ]
  node [
    id 10
    label "Poor_project_execution"
  ]
  node [
    id 11
    label "Non-Delivery_of_benefits"
  ]
  node [
    id 12
    label "Business"
  ]
  edge [
    source 0
    target 1
    relation "deploys"
  ]
  edge [
    source 2
    target 3
    relation "deploys"
  ]
  edge [
    source 4
    target 3
    relation "deploys"
  ]
  edge [
    source 4
    target 5
    relation "deploys"
  ]
  edge [
    source 6
    target 7
    relation "deploys"
  ]
  edge [
    source 8
    target 9
    relation "deploys"
  ]
  edge [
    source 8
    target 3
    relation "deploys"
  ]
  edge [
    source 10
    target 11
    relation "influences"
  ]
  edge [
    source 10
    target 12
    relation "influences"
  ]
]
