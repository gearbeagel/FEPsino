import { defineConfig } from 'vitest/config';

export default defineConfig({
    test: {
        globals: true, // <-- enables global expect, test, describe, etc.
        environment: 'jsdom', // <-- simulates the DOM for React components
        setupFiles: './setupTests.js',
        testTimeout: 10000,
        coverage: {
            provider: 'v8',
            reporter: ['text', 'lcov'],
            reportsDirectory: './coverage',
            exclude: [
                'node_modules/**',
                '**.config.js',
                'src/main.jsx',
                'src/components/user/UserApi.jsx',
                'src/animations/**'
            ]
        },
        reporters: ['default', 'vitest-sonar-reporter'],
        outputFile: {
            json: 'my-json-report.json',
            'vitest-sonar-reporter': 'testResults/sonar-report.xml',
            lcov: 'coverage/lcov.info',
        },
    },
});