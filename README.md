# Git Workflow

Maintaining a clean and organized git workflow is essential for a well running project. This document outlines the git workflow that should be followed by all contributors to help keep the project organized and running smoothly for everyones benefit.

## Forking the Repository

Always fork the repository if you want to contribute. The repository does not allow direct commits or the creation of branches. This is to ensure that the main repository remains clean and organized.  

Before starting, fork the repository to your own account. And start your journey from there.

## Branch Naming

Sometimes it helps maintain an overview if the branches are named in accordance with the issue or feature they are working on. This is not a strict requirement, but it is recommended.

## Commit Message

Commit messages should ALWAYS follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.2/#summary) specification. This is to ensure that the commit messages are clear and easy to understand. The specification is as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

*The commit contains the following structural elements, to communicate intent to the consumers of your library:*
1. *fix: a commit of the type fix patches a bug in your codebase (this correlates with PATCH in semantic versioning).*
2. *feat: a commit of the type feat introduces a new feature to the codebase (this correlates with MINOR in semantic versioning).*
3. *BREAKING CHANGE: a commit that has a footer BREAKING CHANGE:, or appends a ! after the type/scope, introduces a breaking API change (correlating with MAJOR in semantic versioning). A BREAKING CHANGE can be part of commits of any type.*
4. *Others: commit types other than `fix:` and `feat:` are allowed, for example `docs:`, `style:`, `refactor:`, `perf:`, `test:`, and others. We also recommand `improvement` for commits that improve a current implementation without adding a new feature or fixing a bug. Notice these types are not mandated by the conventional commits specification, and have no implicit effect in semantic versioning (unless they include a BREAKING CHANGE, which is NOT recommended). A scope may be provided to a commit’s type, to provide additional contextual information and is contained within parenthesis, e.g., `feat(parser): add ability to parse arrays`.*

### Incorrect Examples

```
<type> description

feat allow provided config object to extend other configs
```
> [!IMPORTANT]  
> Missing colon `:` after the type.

```
<type>: description
Feat: Allow provided config object to extend other configs
```
> [!IMPORTANT]  
> Incorrect capitalization of the type and description.

### Correct Examples

```
<type>: description
feat: allow provided config object to extend other configs
```
> [!NOTE]
> Type in lower case followed by a colon `:` and a description in lower case.

```
<type>[optional scope]: description
test(unit): add validation for config object
```
> [!NOTE]
> Type in lower case followed by a colon `:` and a description in lower case. Optional scope in parenthesis.

## Pull Request

Ideally pull requests should only have a single commit. This is to ensure that the history remains clean and easy to understand. If you have multiple commits, squash them into a single commit before creating the pull request. This way the PR title can be in accordance with the commit message. Which will make it clear what the PR is about. This also is used for the change log, so it is important that the PR title is clear and concise.

```
<type>[optional scope]: <description>
```