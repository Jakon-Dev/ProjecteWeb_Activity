Feature: User login functionality
  As a registered user
  I want to be able to login to the system
  So that I can access protected functionalities

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter username "jordi" and password "betterhealth1"
    And I click on the login button
    Then I should be redirected to the homepage
    And I should see the "Log Out" option

  Scenario: Failed login with invalid credentials
    Given I am on the login page
    When I enter username "invaliduser" and password "invalidpassword"
    And I click on the login button
    Then I should see an error message
    And I should remain on the login page 