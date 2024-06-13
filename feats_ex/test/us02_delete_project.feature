Feature: Delete a project as leader

  Scenario: project does not exist to be deleted
    Given a project "1" with name "PSA-project"
    When the admin deletes a project with id "2"
    Then the admin is notified that the project does not exist

  Scenario: project is deleted
    Given a project "1" with name "PSA-project"
    When the admin deletes a project with id "1"
    Then the project with id "1" is deleted