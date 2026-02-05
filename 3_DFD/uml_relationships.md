# UML Class Diagram - Relationships and Cardinality

## Inheritance Relationships

### 1. Administrator → User (Inheritance)
- **Type:** Generalization/Inheritance
- **Notation:** Empty triangle arrow pointing to parent
- **Description:** Administrator IS-A User (inherits all attributes and methods)
- **Cardinality:** N/A (inheritance relationship)

### 2. GeneralUser → User (Inheritance)
- **Type:** Generalization/Inheritance
- **Notation:** Empty triangle arrow pointing to parent
- **Description:** GeneralUser IS-A User (inherits all attributes and methods)
- **Cardinality:** N/A (inheritance relationship)

## Composition Relationships (Strong "has-a")

### 3. TaskExecutor ◆— ScriptRegistry
- **Type:** Composition (filled diamond)
- **Cardinality:** 1 to 1
- **Description:** TaskExecutor HAS-A ScriptRegistry. The registry's lifetime is bound to the executor.
- **Meaning:** When TaskExecutor is destroyed, ScriptRegistry is also destroyed

### 4. AuditEntry ◆— ExecutionResult
- **Type:** Composition (filled diamond)
- **Cardinality:** 1 to 1
- **Description:** AuditEntry contains exactly one ExecutionResult
- **Meaning:** Each audit log entry owns its execution result; they share the same lifetime

## Aggregation Relationships (Weak "has-a")

### 5. ScriptRegistry ◇— Script
- **Type:** Aggregation (hollow diamond)
- **Cardinality:** 1 to 0..*
- **Description:** ScriptRegistry manages 0 or more Scripts
- **Meaning:** Scripts can exist independently of the registry; registry is a collection

## Association Relationships

### 6. Script — Administrator
- **Type:** Binary Association
- **Cardinality:** 0..* to 1 (many-to-one)
- **Direction:** Script → Administrator (navigable from Script to Admin)
- **Attribute:** Script.registeredBy references the Administrator
- **Description:** Each Script is registered by exactly one Administrator. An Administrator can register 0 or more Scripts.

## Dependency Relationships (uses, creates)

### 7. User ⇢ AuthenticationService
- **Type:** Dependency (dashed arrow with open arrowhead)
- **Stereotype:** «uses»
- **Description:** User depends on AuthenticationService for authentication
- **Nature:** User calls methods on AuthenticationService

### 8. User ⇢ NLPEngine
- **Type:** Dependency
- **Stereotype:** «uses» / submits to
- **Description:** User submits natural language commands to NLPEngine
- **Nature:** User invokes NLPEngine.parseCommand()

### 9. NLPEngine ⇢ ParsedIntent
- **Type:** Dependency
- **Stereotype:** «creates»
- **Description:** NLPEngine creates ParsedIntent objects
- **Nature:** Factory pattern - NLPEngine instantiates ParsedIntent

### 10. ParsedIntent ⇢ ContextManager
- **Type:** Dependency
- **Stereotype:** «used by»
- **Description:** ContextManager uses ParsedIntent to build context
- **Nature:** ContextManager processes ParsedIntent objects

### 11. ContextManager ⇢ TaskExecutor
- **Type:** Dependency
- **Stereotype:** «sends to»
- **Description:** ContextManager sends enriched intents to TaskExecutor
- **Nature:** ContextManager calls TaskExecutor methods with context-enhanced data

### 12. Administrator ⇢ Script
- **Type:** Dependency
- **Stereotype:** «registers»
- **Description:** Administrator registers new Scripts
- **Nature:** Admin.registerScript() creates/adds Script to system

### 13. TaskExecutor ⇢ ExecutionResult
- **Type:** Dependency
- **Stereotype:** «creates»
- **Description:** TaskExecutor creates ExecutionResult objects
- **Nature:** Factory pattern - TaskExecutor instantiates results

### 14. TaskExecutor ⇢ ConfirmationPrompt
- **Type:** Dependency
- **Stereotype:** «creates»
- **Description:** TaskExecutor creates ConfirmationPrompt for write actions
- **Nature:** TaskExecutor instantiates prompts when confirmation needed

### 15. Administrator ⇢ ConfirmationPrompt
- **Type:** Dependency
- **Stereotype:** «confirms»
- **Description:** Administrator responds to confirmation prompts
- **Nature:** Admin.confirmAction() interacts with ConfirmationPrompt

### 16. TaskExecutor ⇢ AuditLogger
- **Type:** Dependency
- **Stereotype:** «logs to»
- **Description:** TaskExecutor logs executions via AuditLogger
- **Nature:** TaskExecutor calls AuditLogger.logExecution()

### 17. AuditLogger ⇢ AuditEntry
- **Type:** Dependency
- **Stereotype:** «creates»
- **Description:** AuditLogger creates AuditEntry objects
- **Nature:** Factory pattern - AuditLogger instantiates log entries

### 18. SelfCorrectionEngine ⇢ ExecutionResult
- **Type:** Dependency
- **Stereotype:** «analyzes»
- **Description:** SelfCorrectionEngine analyzes ExecutionResult on failures
- **Nature:** SelfCorrectionEngine.analyzeError() processes ExecutionResult

### 19. TaskExecutor ⇢ SelfCorrectionEngine
- **Type:** Dependency
- **Stereotype:** «uses on error»
- **Description:** TaskExecutor uses SelfCorrectionEngine when tasks fail
- **Nature:** TaskExecutor calls SelfCorrectionEngine.analyzeError() on failures

### 20. GeneralUser ⇢ CalendarIntegration
- **Type:** Dependency
- **Stereotype:** «uses»
- **Description:** GeneralUser uses CalendarIntegration for scheduling
- **Nature:** GeneralUser calls CalendarIntegration methods

### 21. Administrator ⇢ CalendarIntegration
- **Type:** Dependency
- **Stereotype:** «uses»
- **Description:** Administrator uses CalendarIntegration for scheduling
- **Nature:** Administrator calls CalendarIntegration methods

## Summary of Relationship Types Used

| Relationship Type | Notation | Count | Description |
|------------------|----------|-------|-------------|
| **Inheritance** | Empty triangle | 2 | IS-A relationship (Admin, GeneralUser extend User) |
| **Composition** | Filled diamond | 2 | Strong ownership (TaskExecutor owns ScriptRegistry, AuditEntry owns ExecutionResult) |
| **Aggregation** | Hollow diamond | 1 | Weak ownership (ScriptRegistry contains Scripts) |
| **Association** | Solid line with arrow | 1 | Structural relationship (Script registered by Admin) |
| **Dependency** | Dashed line with arrow | 15 | Uses/Creates relationships |

## Cardinality Notation Used

- **1** : Exactly one
- **0..1** : Zero or one
- **0..*** : Zero or more (unlimited)
- **1..*** : One or more (at least one)
- **n** : Specific number n

## Key Design Patterns Identified

### 1. **Factory Pattern**
- NLPEngine creates ParsedIntent
- TaskExecutor creates ExecutionResult and ConfirmationPrompt
- AuditLogger creates AuditEntry

### 2. **Strategy Pattern**
- ScriptRegistry manages different Script implementations
- Different scripts can be plugged in for different intents

### 3. **Observer Pattern** (Implicit)
- AuditLogger observes TaskExecutor executions
- SelfCorrectionEngine observes execution failures

### 4. **Template Method Pattern**
- User (abstract) defines template methods
- Administrator and GeneralUser provide specific implementations

## Visibility Modifiers

- **+** : public (accessible from anywhere)
- **-** : private (accessible only within the class)
- **#** : protected (accessible within class and subclasses)

## Class Stereotypes

- **«abstract»** : User class (cannot be instantiated)
- **«creates»** : Dependency stereotype indicating creation
- **«uses»** : Dependency stereotype indicating usage
