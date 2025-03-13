export default {
    extends: ['@commitlint/config-conventional'],
    rules: {
        'type-enum': [
            "breaking change",
            "build",
            "chore",
            "ci",
            "docs",
            "feat",
            "fix",
            "perf",
            "refactor",
            "revert",
            "style",
            "test"
        ]
    },
    parserPreset: {
        parserOpts: {
            headerPattern: /^(\w*)!?(?:\((.*)\))?: (.*)$/,
            headerCorrespondence: ['type', 'scope', 'subject'],
            revertPattern: /^(?:Revert|revert:)\s"?([\s\S]+?)"?\s*This reverts commit (\w*)\./i,
            revertCorrespondence: ['header', 'hash']
        }
    }
}