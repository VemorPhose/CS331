# I. Software Architecture Style

**Selected Style:** **Layered Architecture**

The **Nexus Intelligent Chatbot System** is best represented by a **Layered Architecture** style. This approach structures the application into distinct horizontal layers, where each layer has a specific responsibility and interacts only with adjacent layers (e.g., the User Interface layer interacts with the Logic layer, which in turn interacts with Data layers).

### A. Justification of Granularity

The architecture falls into this category because the software components are granularly divided based on their distinct roles in processing a user command:

* **Presentation Layer (User Interaction):**
    * **Components:** CLI or Web-based Chat Interface.
    * **Granularity:** Handles the immediate input/output with the user, strictly separating the "view" from the internal logic.
* **Business Logic Layer (Processing Core):**
    * **Components:** **NLPEngine** (parses intents), **ContextManager** (resolves references), and **TaskExecutor** (orchestrates actions).
    * **Granularity:** This layer encapsulates the system's intelligence. It makes decisions (e.g., determining if a command requires confirmation) without worrying about *how* the data is stored or *how* the script is physically executed.
* **Integration Layer (Service Adaptation):**
    * **Components:** **ScriptRegistry** and **CalendarIntegration**.
    * **Granularity:** Acts as a middleware adapter. It translates internal commands into specific external API calls (e.g., Google Calendar) or executes external Python/Bash scripts, isolating the core system from external dependencies.
* **Data/Persistence Layer:**
    * **Components:** **AuditLogger** and **Database**.
    * **Granularity:** Solely responsible for writing to the immutable audit trail and retrieving user profiles or script metadata.