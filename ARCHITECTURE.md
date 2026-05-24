# Java Kernel Architecture

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Jupyter Notebook UI                      │
│                  (Browser / JupyterLab)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ ZMQ Messages (JSON)
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  Jupyter Kernel Protocol                    │
│              (jupyter_client handles this)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   IPyKernel Framework                       │
│         (provides base kernel infrastructure)               │
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │         JavaKernel (our implementation)           │    │
│  │                                                   │    │
│  │  • do_execute() - main execution handler         │    │
│  │  • _wrap_code_in_class() - code wrapping        │    │
│  │  • _extract_class_name() - parse Java code      │    │
│  │  • send_response() - output to notebook         │    │
│  └───────────────────────┬───────────────────────────┘    │
└────────────────────────────┼────────────────────────────────┘
                             │
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐  ┌──────────────────┐  ┌──────────────┐
│  Create temp  │  │  Compile with    │  │  Execute     │
│  .java file   │─▶│  javac command   │─▶│  with java   │
└───────────────┘  └──────────────────┘  └──────┬───────┘
                                                 │
                                                 │
                                          ┌──────▼───────┐
                                          │   Capture    │
                                          │ stdout/stderr│
                                          └──────┬───────┘
                                                 │
                                                 │
                                          ┌──────▼───────┐
                                          │  Send back   │
                                          │  to notebook │
                                          └──────────────┘
```

## Execution Flow

```
1. User writes code in notebook cell and hits Shift+Enter
         │
         ▼
2. Jupyter sends execute_request message
         │
         ▼
3. JavaKernel.do_execute() is called
         │
         ├─▶ Check if code has class definition
         │   └─▶ No: Wrap in auto-generated class
         │   └─▶ Yes: Use as-is
         │
         ├─▶ Extract class name from code
         │
         ├─▶ Create temporary directory
         │
         ├─▶ Write code to ClassName.java
         │
         ├─▶ Run: javac ClassName.java
         │   ├─▶ Success: Continue
         │   └─▶ Failure: Send compile error to notebook
         │
         ├─▶ Run: java ClassName
         │   ├─▶ Capture stdout → send to notebook
         │   ├─▶ Capture stderr → send to notebook
         │   └─▶ Check exit code
         │
         ├─▶ Clean up temporary files
         │
         ▼
4. Send execute_reply message back to Jupyter
         │
         ▼
5. Notebook displays output to user
```

## Code Wrapping Example

**Input (user code):**
```java
System.out.println("Hello!");
int x = 5;
```

**Transformed to:**
```java
public class JupyterJava1 {
    public static void main(String[] args) {
        System.out.println("Hello!");
        int x = 5;
    }
}
```

**Then compiled and executed**

## Message Flow

```
┌──────────┐                                    ┌──────────┐
│ Notebook │                                    │  Kernel  │
└────┬─────┘                                    └────┬─────┘
     │                                               │
     │  execute_request                             │
     │  {                                           │
     │    "code": "System.out.println(...)",        │
     │    "silent": false                           │
     │  }                                           │
     ├──────────────────────────────────────────────▶
     │                                               │
     │                                               │ Compile & Run
     │                                               │
     │                    stream (stdout)            │
     │  {                                           │
     │    "name": "stdout",                         │
     │    "text": "Hello!"                          │
     │  }                                           │
     ◀──────────────────────────────────────────────┤
     │                                               │
     │                 execute_reply                 │
     │  {                                           │
     │    "status": "ok",                           │
     │    "execution_count": 1                      │
     │  }                                           │
     ◀──────────────────────────────────────────────┤
     │                                               │
```

## File Structure During Execution

```
Temporary Directory (auto-created, auto-deleted)
├── JupyterJava1.java      ← Source code
└── JupyterJava1.class     ← Compiled bytecode
    (deleted after execution)
```

## Key Technologies

- **IPyKernel**: Provides base Kernel class and messaging
- **subprocess**: Runs javac and java commands
- **tempfile**: Creates temporary directories
- **re**: Regular expressions for parsing Java code
- **ZMQ**: Message transport (handled by jupyter_client)

## Error Handling

```
Compilation Error
    │
    ├─▶ Capture stderr from javac
    ├─▶ Send as error traceback
    └─▶ Return status: "error"

Runtime Error
    │
    ├─▶ Capture stderr from java
    ├─▶ Send to stderr stream
    └─▶ Return status: "error"

Timeout (>30 seconds)
    │
    ├─▶ Kill process
    └─▶ Return timeout error
```

## Kernel Lifecycle

```
1. Jupyter starts kernel process
         │
         ▼
2. __main__.py is executed
         │
         ▼
3. IPKernelApp.launch_instance(kernel_class=JavaKernel)
         │
         ▼
4. JavaKernel.__init__() called
         │   └─▶ Check Java installation
         │   └─▶ Initialize state
         ▼
5. Kernel waits for messages
         │
         ├─▶ execute_request → do_execute()
         ├─▶ kernel_info_request → kernel_info()
         ├─▶ shutdown_request → shutdown()
         └─▶ ...
         │
         ▼
6. Kernel runs until shutdown
```

## Integration Points

1. **Jupyter Core**: Manages kernel lifecycle
2. **jupyter_client**: Handles ZMQ messaging
3. **ipykernel**: Provides Kernel base class
4. **Our Code**: JavaKernel implementation
5. **Java Tools**: javac and java commands
6. **OS**: Temporary file system, process management

## Future Enhancement Ideas

1. **Classpath Management**: Support external JARs
2. **Multi-cell State**: Preserve classes across cells
3. **Debugger Integration**: Step through Java code
4. **Code Completion**: Suggest Java methods/classes
5. **Maven/Gradle**: Dependency management
6. **Inspection**: View variables and objects
