import { defineConfig } from 'vitest/config';

export default defineConfig({
    test: {
        globals: true, // <-- enables global expect, test, describe, etc.
        environment: 'jsdom', // <-- simulates the DOM for React components
        setupFiles: './setupTests.js',
        coverage: {
            provider: 'v8',
            reporter: ['text', 'lcov', 'json'],
            reportsDirectory: './coverage',
        },
        reporters: ['default', 'vitest-sonar-reporter'],
        outputFile: {
            json: 'my-json-report.json',
            'vitest-sonar-reporter': 'testResults/sonar-report.xml',
        },
    },
});