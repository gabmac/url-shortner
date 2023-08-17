# **Technical Challenge: URL Shortener**

## **Introduction**
The goal of this challenge is to build a URL shortener similar to platforms like [goo.gl](https://goo.gl/), [shorturl.at](https://www.shorturl.at/), or [bitly.com](https://bitly.com/). The primary use-case for this URL shortener is to facilitate the publishing of promotions on Twitter.

## **Acceptance Criteria**

### **Methodology**
For this challenge, we will be adopting the BDD (Behavior-Driven-Development) methodology. BDD is an extension of TDD (Test-Driven-Development) that emphasizes the behavior of the system.

### **User Stories**
User stories will be structured using the format:
- **"As a [Role], I want [Action], Because [Outcome/Benefit]"**.

This format helps in clearly defining the user's role, the action they want to perform, and the expected outcome or benefit of that action.

### **Acceptance Tests**
Acceptance tests will be written in the **Gherkin** language. The Gherkin language uses keywords like:
- **Scenario**: Defines a particular behavior of the system.
- **Given**: Describes the initial context or state.
- **When**: Describes the action that triggers the behavior.
- **And**: Provides additional conditions or actions.
- **Then**: Describes the expected outcome or result.

Using Gherkin for acceptance tests ensures that the tests are easily readable and can be understood by both technical and non-technical stakeholders.

---

## **User Stories**

1. **URL Lifetime**
    - **As a** system administrator,
    - **I want** to create a short URLs to have an undefined lifetime,
    - **Because** I don't want them to expire automatically.
<br>

1. **Real-time Statistics**
    - **As a** marketer,
    - **I want** access to nearly real-time usage statistics,
    - **Because** I need to monitor the performance of my promotions.
<br>

1. **URL Configuration**
   - **As a** system administrator,
   - **I want** to enable or disable published URLs,
   - **Because** I need control over the accessibility of my content.
   - **As a** system administrator,
   - **I want** to modify the destination URL,
   - **Because** the content I'm promoting might change.
<br>

1. **URL Redirect**
   - **As a** user,
   - **I want** to click on url and be redirect
   - **Because** I want to see the promotion on Twitter


---

## **BDD Scenarios for URL Shortener Platform**

### **Feature: URL Lifetime**
```gherkin
Scenario: Creating a short URL
  Given I need to start a promotion on twitter
  When I give a twitter url
  Then a short url with undefined lifetime should be returned
```

### **Feature: Real-time Statistics**
```gherkin
Scenario: Accessing URL statistics
  Given I have a published short URL
  When I check its statistics
  Then I should see nearly real-time usage data
```

### **Feature: URL Configuration**
```gherkin
Scenario: Enabling a short URL
  Given I have a disabled short URL
  When I enable it
  Then users should be able to access the URL

Scenario: Disabling a short URL
  Given I have an enabled short URL
  When I disable it
  Then users should not be able to access the URL

Scenario: Modifying destination URL
  Given I have a short URL pointing to "old-destination.com"
  When I modify it to point to "new-destination.com"
  Then users accessing the short URL should be redirected to "new-destination.com"
```

---

## **DDD**

In the challenge, we have a very well-defined objective, so we were able to identify only one domain. With the rules and acceptance criteria already defined above, our next step will be to define the entities and value objects."


### **Entities**
- Entities represents a domain objects that are defined by their identity, rather than by their attributes with distinct life cicle


|ShortenedURL|
|--------------|
|original_url: str|
|short_url: str|
|created_at: datetime|
|updated_at: datetime|
|status: StatusEnum|
|statistics: Statistics|

In this Entity we have all data that represents the Shortened Url


### **Value Objects**
- Objects that represent descriptive aspects of the domain with no conceptual identity. 
- Defined by their attributes, does not have identity.
- Usually, Value Objects are small and are used to encapsulate a set of related properties.

|Statistics|
|---|
|amount_of_access: int |

---

### **Routes**

|Endpoint|HTTP Verb|Action|
|---|---|---|
|/create|POST|Create a Short URL|
|/{url_key}|GET|Fowards to target URL|
|/admin/{url_key}|GET|Returns URL data and statistics|
|/admin/{url_key}|PATCH|Update target URL|

---

### **Database Discussion**

**CAP Theorem**

In a distributed computer system, you can only support two of the following guarantees:

 - **Consistency** - Every read receives the most recent write or an error
 - **Availability** - Every request receives a response, without guarantee that it contains the most recent version of the information
 - **Partition Tolerance** - The system continues to operate despite arbitrary partitioning due to network failures

Networks aren't reliable, so you'll need to support partition tolerance. You'll need to make a software tradeoff between consistency and availability.

CP - consistency and partition tolerance
Waiting for a response from the partitioned node might result in a timeout error. CP is a good choice if your business needs require atomic reads and writes.

AP - availability and partition tolerance
Responses return the most readily available version of the data available on any node, which might not be the latest. Writes might take some time to propagate when the partition is resolved.

AP is a good choice if the business needs to allow for eventual consistency or when the system needs to continue working despite external errors.

**Reasons for SQL:**

 - Structured data
 - Strict schema
 - Relational data
 - Need for complex joins
 - Transactions
 - Clear patterns for scaling
 - More established: developers, community, code, tools, etc
 - Lookups by index are very fast

**Reasons for NoSQL:**

 - Semi-structured data
 - Dynamic or flexible schema
 - Non-relational data
 - No need for complex joins
 - Store many TB (or PB) of data
 - Very data intensive workload
 - Very high throughput for IOPS

**Sample data well-suited for NoSQL:**

 - Rapid ingest of clickstream and log data
 - Leaderboard or scoring data
 - Temporary data, such as a shopping cart
 - Frequently accessed ('hot') tables
 - Metadata/lookup tables

Given that the application is going to receive about 10M RPM on peak, and it is a promotion i think the Availability is more important than consistent here, i see the application can relie in eventual consistent where after a write, reads will eventually see it (typically within milliseconds) and ata is replicated asynchronously. So i think that a NoSQL database is well-suited for the problem.

---

### Package Manager

By default, the dependencies are managed with [Poetry](https://python-poetry.org/), go there and install it.

To install poetry you need to run:
```bash
$ curl -sSL https://install.python-poetry.org | python3 -
```
**Note**: Pay Attention here! You may need to change the poetry path on `.bashrc`

From `./<repository>` you can install all the dependencies with:

```bash
$ poetry install
```

Then you can start a shell session with the new environment with:

```bash
$ poetry shell
```

From `./<repository>` you can update all the dependencies with:

```bash
$ poetry update
```

If you want to upgrade poetry you will need to run:
```console
$ poetry self update
```

---

### Pre-Commit and Code Smells

Before **any** commit we run a set of hooks that help us with the quality of the code.

The main code smells are:

1. **Black** - Python Code Formatter
2. **AutoFlake** - Removes Unused Imports
3. **Isort** - Sort Imports
4. **Flake8** - Linting and Checking for Python Errors
5. **Pylint** - Code Analysis for Python
6. **MyPy** - Static Typing for Python
7. **[Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/)** - Force to use correct message for commit

To install you need to run:

```Bash
$ poetry run pre-commit install
```

After that, every commit you execute will run all the hooks.

---

### Docker

To run the project with Docker, it is necessary to have it installed on your machine. If you don't have it, follow the instructions from the links:
- **Ubuntu:** [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- **Mac:** [Install Docker Engine on Mac](https://docs.docker.com/desktop/install/mac-install/)
- **Windows:** [Install Docker Engine on Windows](https://docs.docker.com/desktop/install/windows-install/)


During development, you can change Docker Compose settings that will only affect
the local development environment in the file `docker-compose.yml`.

The changes on that file only affect the local development environment, not
the production environment. So, you can add "temporary" changes that help the
development workflow.

For example, the directory with the backend code is mounted as a Docker
"host volume", mapping the code you change live to the directory inside the container.
That allows you to test your changes right away, without having to build the
Docker image again. It should only be done during development.

For production, you should build the Docker image with a recent version of the
backend code, but during development, it allows you to make changes very fast.

The following commands allows you to get inside your running container and execute
commands inside, for example a Python interpreter to test installed dependencies, or
start the development server that reloads when it detects changes.

To get inside the container with a `bash` session, you can start the stack with:

```bash
$ docker compose up -d
```

and then `exec` inside the running container:

```bash
$ docker compose exec <service> bash
```

You should see an output like:

```console
root@7f2607af31c3:/app#
```

that means that you are in a `bash` session inside your container, as a `root` user,
under the `/code` directory.

---

### Unit Tests and TDD

The project was developed using the Test-Driven Development strategy, which is based on a short cycle of repetitions that consists of Writing the test, Writing the code, and Refactoring the code.

The tests were created based on the acceptance criteria defined above, which were assembled according to the documentation of the challenge.

The tests run on a class-based architecture based on unittest.IsolatedAsyncioTestCase.

To test the backend, run:

```bash
$ poetry run unittest -v
```

To modify and add tests, go to `./<repository>/tests`.

The test will run automatically in the CI.

**Note**: To execute some tests, the database container needs to be up. To do this,
you can run:

```bash
$ docker compose up dynamodb-local
```

#### Test Coverage

Because the test scripts forward arguments to `unittest`, to run the tests in a
running stack with coverage with terminal reports:

```bash
$ poetry run coverage run -m unittest -v
$ poetry run coverage report
```

To generate HTML report runs:

```bash
$ poetry run coverage html
```
---

## Clean Architecture

![image](https://miro.medium.com/v2/resize:fit:720/format:webp/1*0u-ekVHFu7Om7Z-VTwFHvg.png)


Clean architecture is a software architecture pattern proposed by Robert C. Martin, also known as Uncle Bob. It aims to separate concerns within a system, promoting a modular, testable, and easy-to-maintain design.

The main idea behind clean architecture is to establish a clear and defined separation between the different layers of the system, with each layer having specific and well-defined responsibilities. This separation allows the inner layers to be independent of the outer layers, resulting in loose coupling and greater flexibility.

Clean architecture follows the Dependency Inversion Principle (DIP) and the Single Responsibility Principle (SRP), written on [SOLID](https://medium.com/desenvolvendo-com-paixao/o-que-%C3%A9-solid-o-guia-completo-para-voc%C3%AA-entender-os-5-princ%C3%ADpios-da-poo-2b937b3fc530). The Dependency Inversion Principle states that high-level modules should not depend on low-level modules, but on abstractions. The Single Responsibility Principle, on the other hand, asserts that each class or component should have only one reason to change.

### Structure

Clean architecture is composed of several layers, which typically include:

**Domain**: The domain layer is the core of the system and contains the business rules and main entities.

**Application**: The application layer is responsible for orchestrating the actions of the system, applying the business rules of the entity layer.

**Adapter Entrypoints**: This is the layer responsible for dealing with user interaction, whether through a graphical interface, an API, or any other means of communication.

**Infrastructure**: This is the layer responsible for implementing technical details, such as access to databases, calls to external services, etc.