# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue with the owners of this repository before making a change.

Please note we have a [Code of Conduct](CODE-OF-CONDUCT.md), please follow it in all your interactions with the project.

## Built With

- [Flask](https://www.djangoproject.com/) - The Web Framework
- [Mosquitto](https://mosquitto.org/) - MQTT Broker

## How Can I Contribute

### Reporting Issues/Features

This section guides you through submitting a issue for the project. Following these guidelines helps maintainers and the community understand your issue, reproduce the issue and find related issues.

#### Issue Description

  1. Steps to Reproduce:
  2. Expected behavior:
  3. Actual behavior:
  4. Frequency of Occurrence:
  5. Environment configuration:
  6. Additional Information:

Before submitting an issue or feature request, please check the existing issues as your issue might have already been noted.

### Your First Code Contribution

Unsure where to begin contributing to the project? You can start by looking through these `beginner` and `help-wanted` issues:

- Beginner issues - issues which should only require a few lines of code, and a test or two.
- Help wanted issues - issues which should be a bit more involved than `beginner` issues.

#### Local development

Please head over to [README](README.md) to find details about local development.

### Pull Requests

The process described here has several goals:

- Maintain the project's quality
- Fix problems that are important to users
- Engage the community in working in harmony
- Enable a sustainable system for the maintainers to review contributions

Please follow these steps to make your contribution considered:

1. Create a feature branch from `develop`, make changes and raise a PR against it
2. Please make sure that the feature branch is even with the develop branch while raising a PR.
3. Please ensure that all the testcases are passing to make sure that your changes didn't impact any other existing features

While the prerequisites above must be satisfied prior to having your pull request reviewed, the reviewer(s) may ask you to complete additional design work, tests, or other changes before your pull request can be ultimately accepted.

## Styleguides

### Git Commit Messages

- Limit the commit message to 72 characters or less
- Reference issues and pull requests liberally in the commit description
- Consider starting the commit message with an applicable keyword:
  - fix: when fixing a bug
  - feat: when new feature is added
  - test: when updating testcases
  - docs: when docs are updated
  - lint: when lint errors are fixed
  - dep: when any of the dependencies are upgraded
  - chore: for any normal task, which is done as a part of above tasks like updating build scripts, gulp tasks, etc.
