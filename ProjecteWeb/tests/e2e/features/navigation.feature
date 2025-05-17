Feature: Site navigation accessibility
  As a user
  I want to be able to navigate to all main sections of the website
  So that I can access all the features offered

  Scenario: Accessing main pages as an anonymous user
    Given I am not logged in
    When I visit the homepage
    Then I should see the homepage content
    When I go to the agents list page
    Then I should see the agents list


  Scenario: Accessing main pages as an authenticated user
    Given I am logged in as "jordi" with password "betterhealth1"
    When I visit the homepage
    Then I should see the homepage content
    When I go to the agents list page
    Then I should see the agents list
