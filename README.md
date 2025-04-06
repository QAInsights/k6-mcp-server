# 🚀 ⚡️ k6-mcp-server

A Model Context Protocol (MCP) server implementation for running k6 load tests.

## ✨ Features

- Simple integration with Model Context Protocol framework
- Support for custom test durations and virtual users (VUs)
- Easy-to-use API for running k6 load tests
- Configurable through environment variables
- Real-time test execution output

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12 or higher
- k6 load testing tool ([Installation guide](https://grafana.com/docs/k6/latest/set-up/install-k6/))
- uv package manager ([Installation guide](https://github.com/astral-sh/uv))

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/qainsights/k6-mcp-server.git
```

2. Install the required dependencies:

```bash
uv pip install -r requirements.txt
```

3. Set up environment variables (optional):
   Create a `.env` file in the project root:

```bash
K6_BIN=/path/to/k6  # Optional: defaults to 'k6' in system PATH
```

## 🚀 Getting Started

1. Create a k6 test script (e.g., `test.js`):

```javascript
import http from "k6/http";
import { sleep } from "k6";

export default function () {
  http.get("http://test.k6.io");
  sleep(1);
}
```

2. Configure the MCP server using the below specs in your favorite MCP client (Claude Desktop, Cursor, Windsurf and more):

```json
{
  "mcpServers": {
    "k6": {
      "command": "/path/to/bin/uv",
      "args": [
        "--directory",
        "/path/to/k6-mcp-server",
        "run",
        "k6_server.py"
      ]
    }
  }
}

```
3. Now ask the LLM to run the test e.g. `run k6 test for hello.js`. The k6 mcp server will leverage either one of the below tools to start the test.

- `execute_k6_test`: Run a test with default options (30s duration, 10 VUs)
- `execute_k6_test_with_options`: Run a test with custom duration and VUs

![k6-MCP](./images/k6-mcp.png)


## 📝 API Reference

### Execute K6 Test

```python
execute_k6_test(
    script_file: str,
    duration: str = "30s",  # Optional
    vus: int = 10          # Optional
)
```

### Execute K6 Test with Custom Options

```python
execute_k6_test_with_options(
    script_file: str,
    duration: str,
    vus: int
)
```

## ✨ Use cases

- LLM powered results analysis
- Effective debugging of load tests

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
