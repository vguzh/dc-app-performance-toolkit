---
title: "Data Center App Performance Toolkit User Guide For Jira"
platform: platform
product: marketplace
category: devguide
subcategory: build
date: "2024-11-22"
---
# Data Center App Performance Toolkit User Guide For Jira

This document walks you through the process of testing your app on Jira using the Data Center App Performance Toolkit. These instructions focus on producing the required [performance and scale benchmarks for your Data Center app](/platform/marketplace/dc-apps-performance-and-scale-testing/).

{{% note %}}
Data Center App Performance Toolkit is focused on applications performance testing for Marketplace approval process.
For Jira DataCenter functional testing consider [JPT](http://go.atlassian.com/jpt).
{{% /note %}}

In this document, we cover the use of the Data Center App Performance Toolkit on two types of environments:

**[Development environment](#mainenvironmentdev)**: Jira Data Center environment for a test run of Data Center App Performance Toolkit and development of [app-specific actions](#appspecificactions).

1. [Set up a development environment Jira Data Center on AWS](#devinstancesetup).
2. [Run toolkit on the development environment locally](#devtestscenario).
3. [Develop and test app-specific actions locally](#devappaction).

**[Enterprise-scale environment](#mainenvironmententerprise)**: Jira Data Center environment used to generate Data Center App Performance Toolkit test results for the Marketplace approval process.

4. [Set up an enterprise-scale environment Jira Data Center on AWS](#instancesetup).
5. [Setting up load configuration for Enterprise-scale runs](#loadconfiguration).
6. [Running the test scenarios from execution environment against enterprise-scale Jira Data Center](#testscenario).

---

## <a id="mainenvironmentdev"></a>Development environment

Running the tests in a development environment helps familiarize you with the toolkit.
It'll also provide you with a lightweight and less expensive environment for developing app-specific actions.
Once you're ready to generate test results for the Marketplace Data Center Apps Approval process,
run the toolkit in an **enterprise-scale environment**.

---

### <a id="devinstancesetup"></a>1. Setting up Jira Data Center development environment

#### AWS cost estimation for the development environment

{{% note %}}
You are responsible for the cost of AWS services used while running this Terraform deployment.
See [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/) for more detail.
{{% /note %}}

To reduce costs, we recommend you to keep your deployment up and running only during the performance runs.
AWS Jira Data Center development environment infrastructure costs about  20 - 40$ per working week depending on such factors like region, instance type, deployment type of DB, and other.

#### Setup Jira Data Center development environment on k8s.

{{% note %}}
Jira Data Center development environment is good for app-specific actions development.
But not powerful enough for performance testing at scale.
See [Set up an enterprise-scale environment Jira Data Center on AWS](#instancesetup) for more details.
{{% /note %}}

Below process describes how to install low-tier Jira DC with "small" dataset included:

1. Create Access keys for AWS CLI:
   {{% warning %}}
   Do not use `root` user credentials for cluster creation.
   
   **Option 1** (simple): create admin user with `AdministratorAccess` permissions.

   **Option 2** (complex): create granular permission policies with  [policy1](https://raw.githubusercontent.com/atlassian-labs/data-center-terraform/main/permissions/policy1.json) and [policy2](https://raw.githubusercontent.com/atlassian-labs/data-center-terraform/main/permissions/policy2.json).

   The specific configuration relies on how you manage permissions within AWS.
   {{% /warning %}}

   **Example Option 1** with Admin user:
   1. Go to AWS Console -> IAM service -> Users
   2. Create new user -> attach policies directly -> `AdministratorAccess`
   3. Open newly created user -> Security credentials tab -> Access keys -> Create access key -> Command Line Interface (CLI) -> Create access key
   4. Use `Access key` and `Secret access key` in [aws_envs](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/aws_envs) file
   
   **Example Option 2** with granular Policies:
   1. Go to AWS Console -> IAM service -> Policies
   2. Create `policy1` with json content of the [policy1](https://raw.githubusercontent.com/atlassian-labs/data-center-terraform/main/permissions/policy1.json) file
      {{% warning %}}
      **Important**: change all occurrences of `123456789012` to your real AWS Account ID.
      {{% /warning %}}
   3. Create `policy2` with json content of the [policy2](https://raw.githubusercontent.com/atlassian-labs/data-center-terraform/main/permissions/policy2.json) file
      {{% warning %}}
      **Important**: change all occurrences of `123456789012` to your real AWS Account ID.
      {{% /warning %}}
   4. Go to User -> Create user -> Attach policies directly -> Attach `policy1` and `policy2`-> Click on Create user button
   5. Open newly created user -> Security credentials tab -> Access keys -> Create access key -> Command Line Interface (CLI) -> Create access key
   6. Use `Access key` and `Secret access key` in [aws_envs](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/aws_envs) file
2. Clone [Data Center App Performance Toolkit](https://github.com/atlassian/dc-app-performance-toolkit) locally.
   {{% warning %}}
   For annual review, always get the latest version of the DCAPT code from the master branch.

   DCAPT supported versions: three latest minor version [releases](https://github.com/atlassian/dc-app-performance-toolkit/releases).
   {{% /warning %}}
3. Navigate to `dc-app-performance-toolkit/app/util/k8s` folder.
4. Set AWS access keys created in step1 in `aws_envs` file:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_SESSION_TOKEN` (only for temporary creds)
5. Set **required** variables in `dcapt-small.tfvars` file:
   - `environment_name` - any name for you environment, e.g. `dcapt-jira-small`
   - `products` - `jira`
   - `jira_license` - one-liner of valid jira license without spaces and new line symbols
   - `region` - AWS region for deployment. **Do not change default region (`us-east-2`). If specific region is required, contact support.**

   {{% note %}}
   New trial license could be generated on [my atlassian](https://my.atlassian.com/license/evaluation).
   Use `BX02-9YO1-IN86-LO5G` Server ID for generation.
   {{% /note %}}

6. Optional variables to override:
   - `jira_version_tag` - Jira version to deploy. Supported versions see in [README.md](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/README.md).
7. From local terminal (Git Bash for Windows users) start the installation (~20 min):
   ``` bash
   docker run --pull=always --env-file aws_envs \
   -v "/$PWD/dcapt-small.tfvars:/data-center-terraform/conf.tfvars" \
   -v "/$PWD/dcapt-snapshots.json:/data-center-terraform/dcapt-snapshots.json" \
   -v "/$PWD/logs:/data-center-terraform/logs" \
   -it atlassianlabs/terraform:2.9.7 ./install.sh -c conf.tfvars
   ```

8. Copy product URL from the console output. Product url should look like `http://a1234-54321.us-east-2.elb.amazonaws.com/jira`.

{{% note %}}
All the datasets use the standard `admin`/`admin` credentials.
{{% /note %}}

---

### <a id="devtestscenario"></a>2. Run toolkit on the development environment locally

{{% warning %}}
Make sure **English (United States)** language is selected as a default language on the **![cog icon](/platform/marketplace/images/cog.png) &gt; System &gt; General configuration** page. Other languages are **not supported** by the toolkit.
{{% /warning %}}

1. Clone [Data Center App Performance Toolkit](https://github.com/atlassian/dc-app-performance-toolkit) locally.
   {{% warning %}}
   For annual review, always get the latest version of the DCAPT code from the master branch.

   DCAPT supported versions: three latest minor version [releases](https://github.com/atlassian/dc-app-performance-toolkit/releases).
   {{% /warning %}}
1. Follow the [README.md](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/README.md) instructions to set up toolkit locally.
1. Navigate to `dc-app-performance-toolkit/app` folder.
1. Open the `jira.yml` file and fill in the following variables:
   - `application_hostname`: your_dc_jira_instance_hostname without protocol.
   - `application_protocol`: http or https.
   - `application_port`: for HTTP - 80, for HTTPS - 443, 8080, 2990 or your instance-specific port.
   - `secure`: True or False. Default value is True. Set False to allow insecure connections, e.g. when using self-signed SSL certificate.
   - `application_postfix`: `/jira` # e.g. /jira for TerraForm deployment url like `http://a1234-54321.us-east-2.elb.amazonaws.com/jira`. Leave this value blank for url without postfix.
   - `admin_login`: admin user username.
   - `admin_password`: admin user password.
   - `load_executor`: executor for load tests. Valid options are [jmeter](https://jmeter.apache.org/) (default) or [locust](https://locust.io/).
   - `concurrency`: `2` - number of concurrent JMeter/Locust users.
   - `test_duration`: `5m` - duration of the performance run.
   - `ramp-up`: `3s` - amount of time it will take JMeter or Locust to add all test users to test execution.
   - `total_actions_per_hour`: `5450` - number of total JMeter/Locust actions per hour.
   - `WEBDRIVER_VISIBLE`: visibility of Chrome browser during selenium execution (False is by default).

1. Run bzt.

    ``` bash
    bzt jira.yml
    ```

1. Review the resulting table in the console log. All JMeter/Locust and Selenium actions should have 0+% success rate.  
   In case some actions have 0% success rate refer to the following logs in `dc-app-performance-toolkit/app/results/jira/YY-MM-DD-hh-mm-ss` folder:

   - `results_summary.log`: detailed run summary
   - `results.csv`: aggregated .csv file with all actions and timings
   - `bzt.log`: logs of the Taurus tool execution
   - `jmeter.*`: logs of the JMeter tool execution
   - `locust.*`: logs of the Locust tool execution (in case you use Locust as load_executor in jira.yml)
   - `pytest.*`: logs of Pytest-Selenium execution

{{% warning %}}
On the local run with development environment default tests may be flaky due to limited resources of the development cluster and local network.

The only purpose of the development cluster is to [develop app-specific actions](#devappaction).

Do not proceed with the next step if any action has 0% success rate. Ask [support](#support) if above logs analysis did not help.
{{% /warning %}}

---

### <a id="devappaction"></a>3. Develop and test app-specific action locally
Data Center App Performance Toolkit has its own set of default test actions for Jira Data Center: JMeter/Locust and Selenium for load and UI tests respectively.

**App-specific action** - action (performance test) you have to develop to cover main use cases of your application. Performance test should focus on the common usage of your application and not to cover all possible functionality of your app. For example, application setup screen or other one-time use cases are out of scope of performance testing.

1. Define main use case of your app. Usually it is one or two main app use cases.
1. Your app adds new UI elements in Jira Data Center - Selenium app-specific action has to be developed.
1. Your app introduces new endpoint or extensively calls existing Jira Data Center API - JMeter/Locust app-specific actions has to be developed.  
   JMeter and Locust actions are interchangeable, so you could select the tool you prefer:

- JMeter - UI-based [performance tool](https://jmeter.apache.org/).
- Locust - code-based (Python requests library) [performance tool](https://locust.io/).


{{% note %}}
We strongly recommend developing your app-specific actions on the development environment to reduce AWS infrastructure costs.
{{% /note %}}


#### Custom dataset
You can filter your own app-specific issues for your app-specific actions.

1. Create app-specific issues that have specific anchor in summary, e.g. *AppIssue* anchor and issues summaries like *AppIssue1*, *AppIssue2*, *AppIssue3*.
1. Go to the search page of your Jira Data Center - `JIRA_URL/issues/?jql=` and select `Advanced`.
1. Write [JQL](https://www.atlassian.com/blog/jira-software/jql-the-most-flexible-way-to-search-jira-14) that filter just your issues from step 1, e.g. `summary ~ 'AppIssue*'`.
1. Edit Jira configuration file `dc-app-performance-toolkit/app/jira.yml`:
   - `custom_dataset_query:` JQL from step 3.

Next time when you run toolkit, custom dataset issues will be stored to the `dc-app-performance-toolkit/app/datasets/jira/custom-issues.csv` with columns: `issue_key`, `issue_id`, `project_key`.

#### Example of app-specific Selenium action development with custom dataset
You develop an app that adds some additional fields to specific types of Jira issues. In this case, you should develop Selenium app-specific action:

1. Create app-specific Jira issues with *AppIssue* anchor in summary: *AppIssue1*, *AppIssue2*, etc.
2. Go to the search page of your Jira Data Center - `JIRA_URL/issues/?jql=` and check if JQL is correct: `summary  ~ 'AppIssue*'`.
3. Edit `dc-app-performance-toolkit/app/jira.yml` configuration file and set `custom_dataset_query: summary  ~ 'AppIssue*'`.
4. Extend example of app-specific action in `dc-app-performance-toolkit/app/extension/jira/extension_ui.py`.  
   [Code example.](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/extension/jira/extension_ui.py)
   So, our test has to open app-specific issues and measure time to load of this app-specific issues.
5. If you need to run `app_speicifc_action` as specific user uncomment `app_specific_user_login` function in [code example](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/extension/jira/extension_ui.py). Note, that in this case `test_1_selenium_custom_action` should follow just before `test_2_selenium_z_log_out` action.
6. In `dc-app-performance-toolkit/app/selenium_ui/jira_ui.py`, review and uncomment the following block of code to make newly created app-specific actions executed:
``` python
# def test_1_selenium_custom_action(webdriver, datasets, screen_shots):
#     app_specific_action(webdriver, datasets)
```

7. Run toolkit with `bzt jira.yml` command to ensure that all Selenium actions including `app_specific_action` are successful.

#### Example of app-specific Locust/JMeter action development

You develop an app that introduces new GET and POST endpoints in Jira Data Center. In this case, you should develop Locust or JMeter app-specific action.

**Locust app-specific action development example**

1. Extend example of app-specific action in `dc-app-performance-toolkit/app/extension/jira/extension_locust.py`, so that test will call the endpoint with GET request, parse response use these data to call another endpoint with POST request and measure response time.  
   [Code example.](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/extension/jira/extension_locust.py)
1. In `dc-app-performance-toolkit/app/jira.yml` set `load_executor: locust` to make `locust` as load executor.
1. Set desired execution percentage for `standalone_extension`. Default value is `0`, which means that `standalone_extension` action will not be executed. Locust uses actions percentage as relative [weights](https://docs.locust.io/en/stable/writing-a-locustfile.html#weight-attribute), so if `some_action: 10` and `standalone_extension: 20` that means that `standalone_extension` will be called twice more.  
   Set `standalone_extension` weight in accordance with the expected frequency of your app use case compared with other base actions.
1. App-specific tests could be run (if needed) as a specific user. Use `@run_as_specific_user(username='specific_user_username', password='specific_user_password')` decorator for that.
1. Run toolkit with `bzt jira.yml` command to ensure that all Locust actions including `app_specific_action` are successful.

**JMeter app-specific action development example**

1. Check that `jira.yml` file has correct settings of `application_hostname`, `application_protocol`, `application_port`, `application_postfix`, etc.
1. Set desired execution percentage for `standalone_extension`. Default value is `0`, which means that `standalone_extension` action will not be executed.
   For example, for app-specific action development you could set percentage of `standalone_extension` to 100 and for all other actions to 0 - this way only `login_and_view_dashboard` and `standalone_extension` actions would be executed.
1. Navigate to `dc-app-performance-toolkit/app` folder and follow [start JMeter UI README](https://github.com/atlassian/dc-app-performance-toolkit/tree/master/app/util/jmeter#start-jmeter-ui):

   ```python util/jmeter/start_jmeter_ui.py --app jira```

1. Open `Jira` thread group > `actions per login` and navigate to `standalone_extension`
   ![Jira JMeter standalone extension](/platform/marketplace/images/jira-standalone-extension.png)
1. Add GET `HTTP Request`: right-click to `standalone_extension` > `Add` > `Sampler` `HTTP Request`, chose method GET and set endpoint in Path.
   ![Jira JMeter standalone GET](/platform/marketplace/images/jira-standalone-get-request.png)
1. Add `Regular Expression Extractor`: right-click to to newly created `HTTP Request` > `Add` > `Post processor` > `Regular Expression Extractor`
   ![Jira JMeter standalone regexp](/platform/marketplace/images/jira-standalone-regexp.png)
1. Add `Response Assertion`: right-click to newly created `HTTP Request` > `Add` > `Assertions` > `Response Assertion` and add assertion with `Contains`, `Matches`, `Equals`, etc types.
   ![Jira JMeter standalone assertions](/platform/marketplace/images/jira-standalone-assertions.png)
1. Add POST `HTTP Request`: right-click to `standalone_extension` > `Add` > `Sampler` `HTTP Request`, chose method POST, set endpoint in Path and add Parameters or Body Data if needed.
1. Right-click on `View Results Tree` and enable this controller.
1. Click **Start** button and make sure that `login_and_view_dashboard` and `standalone_extension` are successful.
1. Right-click on `View Results Tree` and disable this controller. It is important to disable `View Results Tree` controller before full-scale results generation.
1. Click **Save** button.
1. To make `standalone_extension` executable during toolkit run edit `dc-app-performance-toolkit/app/jira.yml` and set execution percentage of `standalone_extension` accordingly to your use case frequency.
1. App-specific tests could be run (if needed) as a specific user. In the `standalone_extension` uncomment `login_as_specific_user` controller. Navigate to the `username:password` config element and update values for `app_specific_username` and `app_specific_password` names with your specific user credentials. Also make sure that you located your app-specific tests between `login_as_specific_user` and `login_as_default_user_if_specific_user_was_loggedin` controllers.
1. Run toolkit to ensure that all JMeter actions including `standalone_extension` are successful.


##### Using JMeter variables from the base script

Use or access the following variables in your `standalone_extension` script if needed.

- `${issue_key}` - issue key being viewed or modified (e.g. ABC-123)
- `${issue_id}` - issue id being viewed or modified (e.g. 693484)
- `${project_key}` - project key being viewed or modified (e.g. ABC)
- `${project_id}` - project id being viewed or modified (e.g. 3423)
- `${scrum_board_id}` - scrum board id being viewed (e.g. 328)
- `${kanban_board_id}` - kanban board id being viewed (e.g. 100)
- `${jql}` - jql query being used (e.g. text ~ "qrk*" order by key)
- `${username}` - the logged in username (e.g. admin)

{{% warning %}}
App-specific actions are required. Do not proceed with the next step until you have completed app-specific actions development and got successful results from toolkit run.
{{% /warning %}}

---
## <a id="mainenvironmententerprise"></a> Enterprise-scale environment

{{% warning %}}
It is recommended to terminate a development environment before creating an enterprise-scale environment.
Follow [Terminate development environment](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/README.MD#terminate-development-environment) instructions.
In case of any problems with uninstall use [Force terminate command](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/README.MD#force-terminate-cluster).
{{% /warning %}}

After adding your custom app-specific actions, you should now be ready to run the required tests for the Marketplace Data Center Apps Approval process. To do this, you'll need an **enterprise-scale environment**.

### <a id="instancesetup"></a>4. Setting up Jira Data Center enterprise-scale environment with "large" dataset

#### EC2 CPU Limit
{{% warning %}}
The installation of 4-pods DC environment and execution pod requires at least **40** vCPU Cores.
Newly created AWS account often has vCPU limit set to low numbers like 5 vCPU per region.
Check your account current vCPU limit for On-Demand Standard instances by visiting [AWS Service Quotas](https://console.aws.amazon.com/servicequotas/home/services/ec2/quotas/L-1216C47A?region=us-east-2) page.
**Applied quota value** is the current CPU limit in the specific region.

Make that current region limit is large enough to deploy new cluster.
The limit can be increased by using **Request increase at account-level** button: choose a region, set a quota value which equals a required number of CPU Cores for the installation and press **Request** button.
Recommended limit is 50.
{{% /warning %}}

#### AWS cost estimation
[AWS Pricing Calculator](https://calculator.aws/) provides an estimate of usage charges for AWS services based on certain information you provide.
Monthly charges will be based on your actual usage of AWS services and may vary from the estimates the Calculator has provided.

*The prices below are approximate and may vary depending on such factors like region, instance type, deployment type of DB, and other.


| Stack             | Estimated hourly cost ($) |
|-------------------| ------------------------- |
| One pod Jira DC   | 1 - 2
| Two pods Jira DC  | 1.5 - 2
| Four pods Jira DC | 2.0 - 3.0


####  Setup Jira Data Center enterprise-scale environment on k8s

Data dimensions and values for an enterprise-scale dataset are listed and described in the following table.

| Data dimensions | Value for an enterprise-scale dataset |
| --------------- | ------------------------------------- |
| Attachments | ~2 000 000 |
| Comments | ~6 000 000 |
| Components  | ~2 500 |
| Custom fields | ~800 |
| Groups | ~1 000 |
| Issue security levels | 10 |
| Issue types | ~300 |
| Issues | ~1 000 000 |
| Priorities | 5 |
| Projects | 500 |
| Resolutions | 34 |
| Screen schemes | ~200 |
| Screens | ~200 |
| Statuses | ~400 |
| Users | ~21 000 |
| Versions | ~20 000 |
| Workflows | 50 |

{{% note %}}
All the datasets use the standard `admin`/`admin` credentials.
{{% /note %}}

Below process describes how to install enterprise-scale Jira DC with "large" dataset included:

1. Create Access keys for AWS CLI:
   {{% warning %}}
   Do not use `root` user credentials for cluster creation.

   **Option 1** (simple): create admin user with `AdministratorAccess` permissions.

   **Option 2** (complex): create granular permission policies with  [policy1](https://raw.githubusercontent.com/atlassian-labs/data-center-terraform/main/permissions/policy1.json) and [policy2](https://raw.githubusercontent.com/atlassian-labs/data-center-terraform/main/permissions/policy2.json).

   The specific configuration relies on how you manage permissions within AWS.
   {{% /warning %}}

   **Example Option 1** with Admin user:
   1. Go to AWS Console -> IAM service -> Users
   2. Create new user -> attach policies directly -> `AdministratorAccess`
   3. Open newly created user -> Security credentials tab -> Access keys -> Create access key -> Command Line Interface (CLI) -> Create access key
   4. Use `Access key` and `Secret access key` in [aws_envs](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/aws_envs) file

   **Example Option 2** with granular Policies:
   1. Go to AWS Console -> IAM service -> Policies
   2. Create `policy1` with json content of the [policy1](https://raw.githubusercontent.com/atlassian-labs/data-center-terraform/main/permissions/policy1.json) file
      {{% warning %}}
      **Important**: change all occurrences of `123456789012` to your real AWS Account ID.
      {{% /warning %}}
   3. Create `policy2` with json content of the [policy2](https://raw.githubusercontent.com/atlassian-labs/data-center-terraform/main/permissions/policy2.json) file
      {{% warning %}}
      **Important**: change all occurrences of `123456789012` to your real AWS Account ID.
      {{% /warning %}}
   4. Go to User -> Create user -> Attach policies directly -> Attach `policy1` and `policy2`-> Click on Create user button
   5. Open newly created user -> Security credentials tab -> Access keys -> Create access key -> Command Line Interface (CLI) -> Create access key
   6. Use `Access key` and `Secret access key` in [aws_envs](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/aws_envs) file
2. Clone [Data Center App Performance Toolkit](https://github.com/atlassian/dc-app-performance-toolkit) locally.
   {{% warning %}}
   For annual review, always get the latest version of the DCAPT code from the master branch.

   DCAPT supported versions: three latest minor version [releases](https://github.com/atlassian/dc-app-performance-toolkit/releases).
   {{% /warning %}}
3. Navigate to `dc-app-performance-toolkit/app/util/k8s` folder.
4. Set AWS access keys created in step1 in `aws_envs` file:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_SESSION_TOKEN` (only for temporary creds)
5. Set **required** variables in `dcapt.tfvars` file:
   - `environment_name` - any name for you environment, e.g. `dcapt-jira`
   - `products` - `jira`
   - `jira_license` - one-liner of valid jira license without spaces and new line symbols
   - `region` - AWS region for deployment. **Do not change default region (`us-east-2`). If specific region is required, contact support.**

   {{% note %}}
   New trial license could be generated on [my atlassian](https://my.atlassian.com/license/evaluation).
   Use `BX02-9YO1-IN86-LO5G` Server ID for generation.
   {{% /note %}}

6. Optional variables to override:
   - `jira_version_tag` - Jira version to deploy. Supported versions see in [README.md](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/README.md).
7. From local terminal (Git Bash for Windows users) start the installation (~20 min):
   ``` bash
   docker run --pull=always --env-file aws_envs \
   -v "/$PWD/dcapt.tfvars:/data-center-terraform/conf.tfvars" \
   -v "/$PWD/dcapt-snapshots.json:/data-center-terraform/dcapt-snapshots.json" \
   -v "/$PWD/logs:/data-center-terraform/logs" \
   -it atlassianlabs/terraform:2.9.7 ./install.sh -c conf.tfvars
   ```
8. Copy product URL from the console output. Product url should look like `http://a1234-54321.us-east-2.elb.amazonaws.com/jira`.

{{% note %}}
All the datasets use the standard `admin`/`admin` credentials.
It's recommended to change default password from UI account page for security reasons.
{{% /note %}}

---

### <a id="loadconfiguration"></a>5. Setting up load configuration for Enterprise-scale runs

Default TerraForm deployment [configuration](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/dcapt.tfvars)
already has a dedicated execution environment pod to run tests from. For more details see `Execution Environment Settings` section in `dcapt.tfvars` file.

1. Check the `jira.yml` configuration file. If load configuration settings were changed for dev runs, make sure parameters
   were changed back to the defaults:

   ``` yaml
       application_hostname: test_jira_instance.atlassian.com   # Jira DC hostname without protocol and port e.g. test-jira.atlassian.com or localhost
       application_protocol: http      # http or https
       application_port: 80            # 80, 443, 8080, 2990, etc
       secure: True                    # Set False to allow insecure connections, e.g. when using self-signed SSL certificate
       application_postfix: /jira      # e.g. /jira for TerraForm deployment url like `http://a1234-54321.us-east-2.elb.amazonaws.com/jira`. Leave this value blank for url without postfix.
       admin_login: admin
       admin_password: admin
       load_executor: jmeter           # jmeter and locust are supported. jmeter by default.
       concurrency: 200                # number of concurrent virtual users for jmeter or locust scenario
       test_duration: 45m
       ramp-up: 3m                     # time to spin all concurrent users
       total_actions_per_hour: 54500   # number of total JMeter/Locust actions per hour
   ```

You'll need to run the toolkit for each [test scenario](#testscenario) in the next section.

---

### <a id="testscenario"></a>6. Running the test scenarios from execution environment pod against enterprise-scale Jira Data Center

Using the Data Center App Performance Toolkit for [Performance and scale testing your Data Center app](/platform/marketplace/developing-apps-for-atlassian-data-center-products/) involves two test scenarios:

- [Performance regression](#testscenario1)
- [Scalability testing](#testscenario2)

Each scenario will involve multiple test runs. The following subsections explain both in greater detail.

#### <a id="testscenario1"></a> Scenario 1: Performance regression

This scenario helps to identify basic performance issues without a need to spin up a multi-node Jira DC. Make sure the app does not have any performance impact when it is not exercised.

##### <a id="regressionrun1"></a> Run 1 (~50 min)

To receive performance baseline results **without** an app installed:

1. Before run:
   * Make sure `jira.yml` and toolkit code base has default configuration from the `master` branch.
   * Check load configuration parameters needed for enterprise-scale run: [Setting up load configuration for Enterprise-scale runs](#loadconfiguration).
   * Check correctness of `application_hostname`, `application_protocol`, `application_port` and `application_postfix` in .yml file.
   * `standalone_extension` set to 0. App-specific actions are not needed for Run1 and Run2.
   * AWS access keys set in `./dc-app-performance-toolkit/app/util/k8s/aws_envs` file:
      - `AWS_ACCESS_KEY_ID`
      - `AWS_SECRET_ACCESS_KEY`
      - `AWS_SESSION_TOKEN` (only for temporary creds)
1. Navigate to `dc-app-performance-toolkit` folder and start tests execution:
    ``` bash
    export ENVIRONMENT_NAME=your_environment_name
    ```

    ``` bash
    docker run --pull=always --env-file ./app/util/k8s/aws_envs \
    -e REGION=us-east-2 \
    -e ENVIRONMENT_NAME=$ENVIRONMENT_NAME \
    -v "/$PWD:/data-center-terraform/dc-app-performance-toolkit" \
    -v "/$PWD/app/util/k8s/bzt_on_pod.sh:/data-center-terraform/bzt_on_pod.sh" \
    -it atlassianlabs/terraform:2.9.7 bash bzt_on_pod.sh jira.yml
    ```
1. View the results files of the run in the local `dc-app-performance-toolkit/app/results/jira/YY-MM-DD-hh-mm-ss` folder:
   - `results_summary.log`: detailed run summary
   - `results.csv`: aggregated .csv file with all actions and timings
   - `bzt.log`: logs of the Taurus tool execution
   - `jmeter.*`: logs of the JMeter tool execution
   - `pytest.*`: logs of Pytest-Selenium execution

{{% note %}}
Review `results_summary.log` file under artifacts dir location. Make sure that overall status is `OK` before moving to the next steps. For an enterprise-scale environment run, the acceptable success rate for actions is 95% and above.
{{% /note %}}

##### <a id="regressionrun2"></a> Run 2 (~50 min + Lucene Index timing test)

If you are submitting a Jira app, you are required to conduct a Lucene Index timing test. This involves conducting a foreground re-index on a single-node Data Center deployment (with your app installed) and a dataset that has 1M issues.

{{% note %}}
The re-index time for Jira is about ~50-70 minutes.
{{% /note %}}

**Benchmark your re-index time with your app installed:**

1. Install the app you want to test.
2. Setup app license.
3. Go to **![cog icon](/platform/marketplace/images/cog.png) &gt; System &gt; Indexing**.
4. Select the **Full re-index** option.
5. Click **Re-Index** and wait until re-indexing is completed.
   {{% warning %}}
   Jira will be temporarily unavailable during the re-indexing process - "503 Service Temporarily Unavailable" message will be displayed. Once the process is complete, the system will be fully accessible and operational once again.
   {{% /warning %}}

6. **Take a screenshot of the acknowledgment screen** displaying the re-index time and Lucene index timing.
   {{% note %}}
   Re-index information window is displayed on the **Indexing page**. If the window is not displayed, log in to Jira one more time and navigate to **![cog icon](/platform/marketplace/images/cog.png) &gt; System &gt; Indexing**. If you use the direct link to the **Indexing** page, refresh the page after the re-index is finished.
   {{% /note %}}

7. Attach the screenshot(s) to your ECOHELP ticket.

**Performance results generation with the app installed (still use master branch):**

1. Navigate to `dc-app-performance-toolkit` folder and start tests execution:
    ``` bash
    export ENVIRONMENT_NAME=your_environment_name
    ```

    ``` bash
    docker run --pull=always --env-file ./app/util/k8s/aws_envs \
    -e REGION=us-east-2 \
    -e ENVIRONMENT_NAME=$ENVIRONMENT_NAME \
    -v "/$PWD:/data-center-terraform/dc-app-performance-toolkit" \
    -v "/$PWD/app/util/k8s/bzt_on_pod.sh:/data-center-terraform/bzt_on_pod.sh" \
    -it atlassianlabs/terraform:2.9.7 bash bzt_on_pod.sh jira.yml
    ```

{{% note %}}
Review `results_summary.log` file under artifacts dir location. Make sure that overall status is `OK` before moving to the next steps. For an enterprise-scale environment run, the acceptable success rate for actions is 95% and above.
{{% /note %}}


##### Generating a performance regression report

To generate a performance regression report:

1. Edit the `./app/reports_generation/performance_profile.yml` file:
   - For `runName: "without app"`, in the `relativePath` key, insert the relative path to results directory of [Run 1](#regressionrun1).
   - For `runName: "with app"`, in the `relativePath` key, insert the relative path to results directory of [Run 2](#regressionrun2).
1. Navigate locally to `dc-app-performance-toolkit` folder and run the following command from local terminal (Git Bash for Windows users) to generate reports:
    ``` bash
    docker run --pull=always \
    -v "/$PWD:/dc-app-performance-toolkit" \
    --workdir="//dc-app-performance-toolkit/app/reports_generation" \
    --entrypoint="python" \
    -it atlassian/dcapt csv_chart_generator.py performance_profile.yml
    ```
1. In the `./app/results/reports/YY-MM-DD-hh-mm-ss` folder, view the `.csv` file (with consolidated scenario results), the `.png` chart file and performance scenario summary report.
   If you see an impact (>20%) on any action timing, we recommend taking a look into the app implementation to understand the root cause of this delta.

#### <a id="testscenario2"></a> Scenario 2: Scalability testing

The purpose of scalability testing is to reflect the impact on the customer experience when operating across multiple nodes.
For this, you have to run scale testing on your app.

For many apps and extensions to Atlassian products,
there should not be a significant performance difference between operating on a single node or across many nodes in
Jira DC deployment. To demonstrate performance impacts of operating your app at scale, we recommend testing your Jira DC app in a cluster.


###### <a id="run3"></a> Run 3 (~50 min)

To receive scalability benchmark results for one-node Jira DC **with** app-specific actions:

1. Before run:
   * Make sure `jira.yml` and toolkit code base has code base with your developed app-specific actions.
   * Check correctness of `application_hostname`, `application_protocol`, `application_port` and `application_postfix` in .yml file.
   * Check load configuration parameters needed for enterprise-scale run: [Setting up load configuration for Enterprise-scale runs](#loadconfiguration).
   * `standalone_extension` set to non 0 and .jmx file has standalone actions implementation in case of JMeter app-specific actions.
   * [test_1_selenium_custom_action](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/selenium_ui/jira_ui.py#L65-L66) is uncommented and has implementation in case of Selenium app-specific actions.
   * AWS access keys set in `./dc-app-performance-toolkit/app/util/k8s/aws_envs` file:
      - `AWS_ACCESS_KEY_ID`
      - `AWS_SECRET_ACCESS_KEY`
      - `AWS_SESSION_TOKEN` (only for temporary creds)
1. Navigate to `dc-app-performance-toolkit` folder and start tests execution:
    ``` bash
    export ENVIRONMENT_NAME=your_environment_name
    ```

    ``` bash
    docker run --pull=always --env-file ./app/util/k8s/aws_envs \
    -e REGION=us-east-2 \
    -e ENVIRONMENT_NAME=$ENVIRONMENT_NAME \
    -v "/$PWD:/data-center-terraform/dc-app-performance-toolkit" \
    -v "/$PWD/app/util/k8s/bzt_on_pod.sh:/data-center-terraform/bzt_on_pod.sh" \
    -it atlassianlabs/terraform:2.9.7 bash bzt_on_pod.sh jira.yml
    ```

{{% note %}}
Review `results_summary.log` file under artifacts dir location. Make sure that overall status is `OK` before moving to the next steps. For an enterprise-scale environment run, the acceptable success rate for actions is 95% and above.
{{% /note %}}


##### <a id="run4"></a> Run 4 (~50 min)
{{% note %}}
Before scaling your DC make sure that AWS vCPU limit is not lower than needed number. Minimum recommended value is 50.
Use [AWS Service Quotas service](https://console.aws.amazon.com/servicequotas/home/services/ec2/quotas/L-1216C47A?region=us-east-2) to see current limit for `us-east-2` region.
[EC2 CPU Limit](https://developer.atlassian.com/platform/marketplace/dc-apps-performance-toolkit-user-guide-jira/#ec2-cpu-limit) section has instructions on how to increase limit if needed.
{{% /note %}}

To receive scalability benchmark results for two-node Jira DC **with** app-specific actions:

1. Navigate to `dc-app-performance-toolkit/app/util/k8s` folder.
1. Open `dcapt.tfvars` file and set `jira_replica_count` value to `2`.
1. From local terminal (Git Bash for Windows users) start scaling (~20 min):
   ``` bash
   docker run --pull=always --env-file aws_envs \
   -v "/$PWD/dcapt.tfvars:/data-center-terraform/conf.tfvars" \
   -v "/$PWD/dcapt-snapshots.json:/data-center-terraform/dcapt-snapshots.json" \
   -v "/$PWD/logs:/data-center-terraform/logs" \
   -it atlassianlabs/terraform:2.9.7 ./install.sh -c conf.tfvars
   ```
1. Navigate to `dc-app-performance-toolkit` folder and start tests execution:
    ``` bash
    export ENVIRONMENT_NAME=your_environment_name
    ```

    ``` bash
    docker run --pull=always --env-file ./app/util/k8s/aws_envs \
    -e REGION=us-east-2 \
    -e ENVIRONMENT_NAME=$ENVIRONMENT_NAME \
    -v "/$PWD:/data-center-terraform/dc-app-performance-toolkit" \
    -v "/$PWD/app/util/k8s/bzt_on_pod.sh:/data-center-terraform/bzt_on_pod.sh" \
    -it atlassianlabs/terraform:2.9.7 bash bzt_on_pod.sh jira.yml
    ```

{{% note %}}
Review `results_summary.log` file under artifacts dir location. Make sure that overall status is `OK` before moving to the next steps. For an enterprise-scale environment run, the acceptable success rate for actions is 95% and above.
{{% /note %}}


##### <a id="run5"></a> Run 5 (~50 min)
{{% note %}}
Before scaling your DC make sure that AWS vCPU limit is not lower than needed number. Minimum recommended value is 50.
Use [AWS Service Quotas service](https://console.aws.amazon.com/servicequotas/home/services/ec2/quotas/L-1216C47A?region=us-east-2) to see current limit for `us-east-2` region.
[EC2 CPU Limit](https://developer.atlassian.com/platform/marketplace/dc-apps-performance-toolkit-user-guide-jira/#ec2-cpu-limit) section has instructions on how to increase limit if needed.
{{% /note %}}

To receive scalability benchmark results for four-node Jira DC with app-specific actions:

1. Scale your Jira Data Center deployment to 4 nodes as described in [Run 4](#run4).
1. Navigate to `dc-app-performance-toolkit` folder and start tests execution:
    ``` bash
    export ENVIRONMENT_NAME=your_environment_name
    ```

    ``` bash
    docker run --pull=always --env-file ./app/util/k8s/aws_envs \
    -e REGION=us-east-2 \
    -e ENVIRONMENT_NAME=$ENVIRONMENT_NAME \
    -v "/$PWD:/data-center-terraform/dc-app-performance-toolkit" \
    -v "/$PWD/app/util/k8s/bzt_on_pod.sh:/data-center-terraform/bzt_on_pod.sh" \
    -it atlassianlabs/terraform:2.9.7 bash bzt_on_pod.sh jira.yml
    ```

{{% note %}}
Review `results_summary.log` file under artifacts dir location. Make sure that overall status is `OK` before moving to the next steps. For an enterprise-scale environment run, the acceptable success rate for actions is 95% and above.
{{% /note %}}


#### Generating a report for scalability scenario

To generate a scalability report:

1. Edit the `./app/reports_generation/scale_profile.yml` file:
   - For `runName: "1 Node"`, in the `relativePath` key, insert the relative path to results directory of [Run 3](#run3).
   - For `runName: "2 Nodes"`, in the `relativePath` key, insert the relative path to results directory of [Run 4](#run4).
   - For `runName: "4 Nodes"`, in the `relativePath` key, insert the relative path to results directory of [Run 5](#run5).
1. Navigate locally to `dc-app-performance-toolkit` folder and run the following command from local terminal (Git Bash for Windows users) to generate reports:
    ``` bash
    docker run --pull=always \
    -v "/$PWD:/dc-app-performance-toolkit" \
    --workdir="//dc-app-performance-toolkit/app/reports_generation" \
    --entrypoint="python" \
    -it atlassian/dcapt csv_chart_generator.py scale_profile.yml
    ```
1. In the `./app/results/reports/YY-MM-DD-hh-mm-ss` folder, view the `.csv` file (with consolidated scenario results), the `.png` chart file and performance scenario summary report.
   If you see an impact (>20%) on any action timing, we recommend taking a look into the app implementation to understand the root cause of this delta.

{{% warning %}}
It is recommended to terminate an enterprise-scale environment after completing all tests.
Follow [Terminate enterprise-scale environment](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/README.MD#terminate-enterprise-scale-environment) instructions.
In case of any problems with uninstall use [Force terminate command](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/README.MD#force-terminate-cluster).
{{% /warning %}}

#### Attaching testing results to ECOHELP ticket

{{% warning %}}
Do not forget to attach performance testing results to your ECOHELP ticket.
{{% /warning %}}

1. Make sure you have two reports folders: one with performance profile and second with scale profile results.
   Each folder should have `profile.csv`, `profile.png`, `profile_summary.log` and profile run result archives. Archives
   should contain all raw data created during the run: `bzt.log`, selenium/jmeter/locust logs, .csv and .yml files, etc.
2. Attach two reports folders to your ECOHELP ticket.

## <a id="support"></a> Support
If the installation script fails on installing Helm release or any other reason, collect the logs, zip and share to [community Slack](http://bit.ly/dcapt_slack) **#data-center-app-performance-toolkit** channel.
For instructions on how to collect detailed logs, see [Collect detailed k8s logs](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/README.MD#collect-detailed-k8s-logs).
For failed cluster uninstall use [Force terminate command](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/README.MD#force-terminate-cluster).

In case of any technical questions or issues with DC Apps Performance Toolkit, contact us for support in the [community Slack](http://bit.ly/dcapt_slack) **#data-center-app-performance-toolkit** channel.
