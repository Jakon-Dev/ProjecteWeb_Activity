Feature: Comment management on agents
  As a registered user
  I want to be able to create, edit and delete a comment on an agent

  Scenario: Create a new comment
    Given I am logged in as "jordi" with password "betterhealth1"
    And I go to the agent detail page for agent with name "Phoenix"
    When I submit a new comment "Great agent"
    Then I should see the comment "Great agent"
    When I submit a new comment "Amazing abilities"
    Then I should see the comment "Amazing abilities"

  Scenario: Edit my comment
    Given I am logged in as "jordi" with password "betterhealth1"
    And I have previously added the comment "Amazing abilities"
    When I edit the comment to "Edited comment"
    Then I should see the comment "Edited comment"

  Scenario: Delete my comment
    Given I am logged in as "jordi" with password "betterhealth1"
    And I have previously added the comment "Edited comment"
    When I delete the comment
    Then I should not see the comment "Edited comment"
