## `/frontend`

React-based UI for the system.

### `/frontend/public`

Static assets like logos, manifest files, favicon.

### `/frontend/src`

Main app logic and views.

* `App.jsx`: Root component
* `main.jsx`: React DOM render entrypoint

#### `/frontend/src/pages`

Main pages.

* `Login.jsx`: Login form UI
* `Register.jsx`: User signup form
* `Home.jsx`: Dashboard with chat and task panels

#### `/frontend/src/components`

Reusable components.

* `ChatInterface.jsx`: Main chat screen with bot
* `FileUploader.jsx`: Upload area for documents
* `Dashboard.jsx`: Widgets showing tasks, docs, and status

#### `/frontend/src/components/Auth`

Auth-specific UI components (e.g., input forms, reset flows).

#### `/frontend/src/api`

Axios wrappers for backend API endpoints (auth, chat, files, etc).

#### `/frontend/src/context`

React Context APIs (e.g., user session provider, chat context).


`Kigen, I don't know how this whole front end things works, but here is what chatgpt did`