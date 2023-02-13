Feature: Test Python skills and web protocol knowledge
  In order to check the person professional skills,
  As a TOHT Tech Lead
  I want my developers to be able to understand, modify and write code and tests
  On python language based on their skill levels
  So that i need to understand this level.

Scenario Outline: HTTP requests to the server
   Given I perform <method> request to the server <url> with <header>
   Then I have response with <status> code and content contains <content>

 Examples: Amphibians
   | method | url   | header  | status | content          |
   | GET    | /     |  FOO    | 200    |   MAIN PAGE      |
   | GET    | /blog |  AUTH   | 200    |   Blog Page      |
   | GET    | /blog |  BAR    | 403    |   Blog Page      |
   | GET    | /     |  AUTH   | 200    |   MAIN PAGE      |
