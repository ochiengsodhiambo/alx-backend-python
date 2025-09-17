## Unit Tests and Integration Tests 
The tatsks herein are undertakem to enhance the undetanding of:
- Tha difference between unit and integration tests.
- Common testing patterns such as mocking, parametrizations and fixtures

### Files:
### test_utils.py
test_access_nested_map_exception
   - Uses @parameterized.expand
   - Asserts KeyError
   - Checks error message equals repr(path[-1])
TestGetJson
   - Uses unittest.mock.patch to replace requests.get
   - Returns a Mock with .json()
   - Ensures: requests.get called once & Return matches expected payload
TestMemoize
   - Defines TestClass with @memoize
   - Patches a_method
   - Verifies: Return value is correct & Method is only called once even with the existence of 2 property accesses

### test_client.py
Allows one to move from unit testing and get into a mix of unit and integration testing with fixtures and client code.

TestGithubOrgClient.test_org
   - Parametrized (google, abc)
   - Patches client.get_json
   - Asserts return matches payload
   - Asserts called once with expected URL

test_public_repos_url
   - Patches .org property with PropertyMock
   - Ensures _public_repos_url returns correct URL

test_public_repos
   - Patches get_json (returns fake repo payload)
   - Patches _public_repos_url (returns dummy URL)
   - Asserts repos list matches expected

test_has_license
   - Parametrized with two repo dicts
   - Checks return values True and False

Integration Tests with Fixtures
   - Uses @parameterized_class with fixtures.py
   - setUpClass starts requests.get patcher with side_effect returning fixtures
   - tearDownClass stops patcher
   - Tests:  public_repos returns expected repos list & public_repos(license="apache-2.0") filters correctly
  
