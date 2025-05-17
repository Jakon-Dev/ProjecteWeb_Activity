Feature: User registration functionality
  As a visitor
  I want to be able to register a new account
  So that I can access protected features of the site

  Scenario: Successful registration with valid data
    Given I am on the register page
    When I enter registration details:
      | username     | email               | password      | password2     |
      | newusertest  | newuser@example.com | Securepass123 | Securepass123 |
    And I click on the register button
    Then I should be redirected to the login page
    And I should see a registration success message

  Scenario: Failed registration with existing username
    Given I am on the register page
    And a user with username "jordi" already exists
    When I enter registration details:
      | username | email               | password      | password2     |
      | jordi    | newuser@example.com | securepass123 | securepass123 |
    And I click on the register button
    Then I should see an error message about existing username
    And I should remain on the register page

  Scenario: Failed registration with mismatched passwords
    Given I am on the register page
    When I enter registration details:
        | username     | email               | password        | password2        |
        | wrongpass1   | wrong1@example.com  | securepass123   | differentpass123 |
    And I click on the register button
    Then I should see an error message about password mismatch
    And I should remain on the register page