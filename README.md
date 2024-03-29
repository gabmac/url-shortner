[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![poetry](https://img.shields.io/badge/maintained%20with-poetry-rgb(30%2041%2059).svg)](https://python-poetry.org/)

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

# **Technical Challenge: URL Shortener**

## **Introduction**
The goal of this challenge is to build a URL shortener similar to platforms like [goo.gl](https://goo.gl/), [shorturl.at](https://www.shorturl.at/), or [bitly.com](https://bitly.com/). The primary use-case for this URL shortener is to facilitate the publishing of promotions on Twitter.


## Constraints

  1. 1M RPM peaks of traffic
  2. 99.98% uptime

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

2. **URL Configuration**
   - **As a** system administrator,
   - **I want** to enable or disable published URLs,
   - **Because** I need control over the accessibility of my content.
   - **As a** system administrator,
   - **I want** to modify the destination URL,
   - **Because** the content I'm promoting might change.
<br>

3. **URL Redirect**
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
|status: ShortUrlStatusEnum|

In this Entity we have all data that represents the Shortened Url

---

### **Routes**

|Endpoint|HTTP Verb|Action|
|---|---|---|
|admin/create|POST|Create a Short URL|
|/admin|GET|List All Short URLs|
|/admin/{url_key}|PATCH|Update target URL|
|/{url_key}|GET|Fowards to target URL|
|/docs|GET|Swagger|

---

### **Infrastructure Discussion**

It's import to point out that a *Multi-AZ infrastructure* would give more resiliency to the application, make the system robust in case of a disaster.

<img src="./infrastructure.svg">

##### *Short Description*


  1. Incoming requests are first received by an Elastic Load Balancer (ELB).
  2. The ELB routes the requests to an ECS cluster, which is hosted on EC2 instances.Both the ECS cluster and the EC2 instances have auto-scaling rules in place to dynamically adjust capacity based on demand.
  3. The ECS tasks, responsible for processing the requests, run containerized applications. The container images for these tasks are stored in and pulled from Amazon Elastic Container Registry (ECR).
  4. The application uses Amazon DynamoDB as its primary database.
  5. Application request logs are forwarded to an OpenSearch cluster using Logstash.
  6. DataDog is employed to monitor and manage both application and infrastructure metrics.
#### **Database Discussion**

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

**Key-value store**

Abstraction: hash table

A key-value store generally allows for O(1) reads and writes and is often backed by memory or SSD. Data stores can maintain keys in lexicographic order, allowing efficient retrieval of key ranges. Key-value stores can allow for storing of metadata with a value.

Key-value stores provide high performance and are often used for simple data models or for rapidly-changing data. Since they offer only a limited set of operations, complexity is shifted to the application layer if additional operations are needed.

##### **Result**

Given that the application is going to receive about 10M RPM on peak, and it is a redirect application i think the Availability is more important than consistent here, i see the application can relie in eventual consistent where after a write, reads will eventually see it (typically within milliseconds) and data is replicated asynchronously. So i think that a **NoSQL** database is well-suited for the problem.

As explained above a Key-value Store Datrabase can be a really eficient for the purpose of this application so the Database chosen is **DynamoDb** .

###### [**DynamoDb**](https://aws.amazon.com/pm/dynamodb/?nc1=h_ls)
Handle 10 Trillion Request Per day
Peaks = 20 Million Request Second
Uptime = 99.999%

If needed we can use [DAX](https://aws.amazon.com/dynamodb/dax/) as caching service to delivery more perfomance improvement - from milisecondes to microseconds. But It's important to know that it will affect cost.

#### Image Repository

For Container Image Repository we can use [ECR](https://aws.amazon.com/ecr/?nc1=h_ls)

#### Monitoring

For Requests and log processing we can use ElasticSearch or AWS OpenSearch. We can add a logstash. Sending events to Logstash lets you decouple event processing from your app. Your app only needs to send events to Logstash and doesn’t need to know anything about what happens to the events afterwards.
Other option to logstash is Kinesis FireHose combined with OpenSearch, Kinesis will try to load data on OpenSearch if its fail it will write a document on S3 as contingency

With we want to monitoring metrics as CPU and memory too besides logs, we can use DataDog or AWS CloudWatch.

#### Load Balancer

Load balancers distribute incoming client requests to computing resources such as application servers and databases. In each case, the load balancer returns the response from the computing resource to the appropriate client.

Uptime=99.99%

#### Host

For Container Orchestration we can choose between  [Amazon Elastic Container Service(ECS)](https://aws.amazon.com/ecs/?pg=ln&sec=hiw) or [Amazon Elastic Kubernetes Service(EKS)](https://aws.amazon.com/eks/?pg=ln&sec=hiw). The one choosen is ECS. Amazon Elastic Container Service (Amazon ECS) is a fully managed container orchestration service that simplifies your deployment, management, and scaling of containerized applications. Simply describe your application and the resources required, and Amazon ECS will launch, monitor, and scale your application across flexible compute options with automatic integrations to other supporting AWS services that your application needs. Perform system operations such as creating custom scaling and capacity rules, and observe and query data from application logs and telemetry.

With ECS we can use?
  1. [AWS Fargate](https://aws.amazon.com/fargate/?nc1=h_ls) is a serverless, pay-as-you-go compute engine that lets you focus on building applications without managing servers. A pitfall is that as a serverless applcation it can increase the cost.
  2. We would use ECS with EC2, it would reduce the cost compared with Fargate, but we would need to pay attention in EC2 scalling.
  3. Other option would be [EC2 Spot Instance](https://aws.amazon.com/pt/ec2/spot/) that could reduce significantly, but there is a average high frequency of interruption. So the application uptime wouldn't be respected.


The chosen one is ECS+EC2.

Uptime = 99.99%

#### Availability in numbers
Availability is often quantified by uptime (or downtime) as a percentage of time the service is available. Availability is generally measured in number of 9s--a service with 99.99% availability is described as having four 9s.

**Availability in parallel vs in sequence**
If a service consists of multiple components prone to failure, the service's overall availability depends on whether the components are in sequence or in parallel.

##### *In Sequence*

Overall availability decreases when two components with availability < 100% are in sequence:

```math
Availability (Total) = Availability (Foo) * Availability (Bar)
```

##### *In Parallel*

Overall availability increases when two components with availability < 100% are in parallel:

```math
Availability (Total) = 1 - (1 - Availability (Foo)) * (1 - Availability (Bar))
```

##### **Result**
```math
Availability (Total) = Availability (DynamoDb) * Availability (Fargate+ECS) * Availability (Load Balance)
```

```math
Availability (Total) = 99.999 * 99.99 * 99.99 = 99.97 > 99.95
```
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
8. **Bandit** -  Designed to find common security issues in Python code
9. **Pip Audit** - Tool for scanning Python environments for packages with known vulnerabilities

To install you need to run:

```Bash
$ poetry run pre-commit install
```

After that, every commit you execute will run all the hooks.

---

### Docker

Docker is an open-source platform that automates the deployment, scaling, and management of applications. It does this through containerization, a lightweight form of virtualization.

Containers can be thought of as isolated environments where applications can run. They include everything that an application needs to run, including the code, runtime, system tools, libraries, and settings. This means that the application will run the same way regardless of the environment it's in.

The key advantages of Docker include:

  1. Consistency: Since a Docker container bundles its own software, libraries, and dependencies, it ensures consistency across multiple development, testing, and production environments.

  2. Isolation: Containers are isolated from each other and from the host system, improving security and allowing multiple containers to run on the same system without interfering with each other.

  3. Portability: Containers can be run on any system that supports Docker, making it easy to deploy applications across multiple environments or cloud platforms.

  4. Scalability: Multiple containers can be run on a single host, and containers can be easily added or removed as needed, making Docker highly scalable.

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

To initialize the application, first you need it to build:

```bash
$ docker compose -f docker-compose.dev.yml build
```

Then run:

```bash
$ docker compose -f docker-compose.dev.yml up
```

Be sure that OpenSearch Node is up, what else the api can returns 500.


.env
```env
AWS_DEFAULT_REGION=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```


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
$ docker compose -f docker-compose.dev.yml up dynamodb-local
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

You can use `docker compose` to run tests too:

```bash
$ docker compose -f docker-compose.test.yml build
$ docker compose -f docker-compose.test.yml up
```

***Report***


|Name|Stmts|Miss|Branch|BrPart|Cover|
|---|---|---|---|---|---|
system/infrastructure/adapters/entrypoints/api/routes/base_route.py|4|0|0|0|100%|
system/infrastructure/adapters/database/repositories/short_url_repository.py|16|0|2|0|100%|
system/application/usecase/short_url/update_short_url_usecase.py|21|0|4|0|100%|
system/application/usecase/short_url/redirect_short_url_usecase.py|16|0|0|0|100%|
system/application/usecase/short_url/query_short_url_usecase.py|11|0|2|0|100%|
system/application/usecase/short_url/create_short_url_usecase.py|21|0|0|0|100%|
system/application/usecase/short_url/basic_behavior_usecase.py|5|0|2|0|100%|
system/infrastructure/adapters/entrypoints/api/routes/short_url/redirect_short_url.py|21|0|2|1|96%|
system/infrastructure/adapters/entrypoints/api/routes/admin/update_short_url_view.py|21|0|2|1|96%|
system/infrastructure/adapters/entrypoints/api/routes/admin/create_short_url_view.py|17|0|2|1|95%|
system/infrastructure/adapters/entrypoints/api/routes/admin/query_short_url_view.py|16|0|2|1|94%|
system/infrastructure/adapters/entrypoints/api/routes/short_url/base_short_url_view.py|7|0|2|1|89%|
system/infrastructure/adapters/entrypoints/api/routes/admin/base_admin_short_url_view.py|7|0|2|1|89%|
|---|---|---|---|---|---|
|TOTAL|183|0|22|6|97%|

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

**Infrastructure**: This is the layer responsible for implementing technical details, such as access to databases, calls to external services, etc.
