Feature: Create a project
  Scenario: Project created successfully
    Given the projects
      |      name           | objective                                               | deadline      | leader  | aprox_time | status      |
      | CORE_ERP_v12        | add features to configurate a flexible cost calculator  | 2024-12-31    | Isaias  | 120h       | in progress |
      | PROYECTS_SERVICE_v2 | add feature to interact with ERP to estimate costs      | 2024-07-25    | None    | 70h        | NEW         |
    And the employees
      | name    | worker_number |
      | Isaias  | 1             |
    When the admin creates a project with name "CORE_PHYSICS_ENG_v2"
    Then the project with name "CORE_PHYSICS_ENG_v2" is created

  Scenario: Project with same name already exists
    Given the projects
      |      name           | objective                                               | deadline      | leader  | aprox_time | status      |
      | CORE_ERP_v12        | add features to configurate a flexible cost calculator  | 2024-12-31    | Isaias  | 120h       | in progress |
      | PROYECTS_SERVICE_v2 | add feature to interact with ERP to estimate costs      | 2024-07-25    | None    | 70h        | NEW         |
    And the employees
      | name    | worker_number |
      | Isaias  | 1             |
    When the admin creates a project with name "CORE_ERP_v12"
    Then the admin is notified that the project already exists and duplicates are not allowed
