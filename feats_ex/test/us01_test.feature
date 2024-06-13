Feature: Assign a project leader

  Scenario: Proyect does not exist
    Given the projects
      |      name           | objective                                               | deadline      | leader  | aprox_time | status      |
      | CORE_ERP_v12        | add features to configurate a flexible cost calculator  | 2024-12-31    | Isaias  | 120h       | in progress |
      | PROYECTS_SERVICE_v2 | add feature to interact with ERP to estimate costs      | 2024-07-25    | None    | 70h        | NEW         |
    And the employees
      | name    | worker_number |
      | Isaias  | 1             |
      | Marcelo | 2             |
    When the admin assigns "Isaias" as the leader of "CORE_PHYSICS_ENG_v2.1"
    Then the admin is notified that the project does not exist

  Scenario: Worker does not exist
    Given the projects
      |      name           | objective                                               | deadline      | leader  | aprox_time | status      |
      | CORE_ERP_v12        | add features to configurate a flexible cost calculator  | 2024-12-31    | Isaias  | 120h       | in progress |
      | PROYECTS_SERVICE_v2 | add feature to interact with ERP to estimate costs      | 2024-07-25    | None    | 70h        | NEW         |
    And the employees
      | name    | worker_number |
      | Isaias  | 1             |
      | Marcelo | 2             |
    When the admin assigns "Juan" as the leader of "PROYECTS_SERVICE_v2"
    Then the admin is notified that the given project leader does not exist

  Scenario: Leader already assigned
    Given the projects
      |      name           | objective                                               | deadline      | leader  | aprox_time | status      |
      | CORE_ERP_v12        | add features to configurate a flexible cost calculator  | 2024-12-31    | Isaias  | 120h       | in progress |
      | PROYECTS_SERVICE_v2 | add feature to interact with ERP to estimate costs      | 2024-07-25    | None    | 70h        | NEW         |
    And the employees
      | name    | worker_number |
      | Isaias  | 1             |
      | Marcelo | 2             |
    When the admin assigns "Marcelo" as the leader of "CORE_ERP_v12"
    Then the admin is notified that the project already has a leader

  Scenario: Leader assigned successfully
    Given the projects
      |      name           | objective                                               | deadline      | leader  | aprox_time | status      |
      | CORE_ERP_v12        | add features to configurate a flexible cost calculator  | 2024-12-31    | Isaias  | 120h       | in progress |
      | PROYECTS_SERVICE_v2 | add feature to interact with ERP to estimate costs      | 2024-07-25    | None    | 70h        | NEW         |
    And the employees
      | name    | worker_number |
      | Isaias  | 1             |
      | Marcelo | 2             |    
    When the admin assigns "Marcelo" as the leader of "PROYECTS_SERVICE_v2"
    Then "Marcelo" is added as the leader of "PROYECTS_SERVICE_v2"
