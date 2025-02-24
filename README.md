# first thing you have to ensure
 1 ki yaha "backend" ka folder bekaar hai delete nhi ho rha...to ignore maaro...usko
 2 ki "backendd" ye hai sahi wala folder jisme poora backend hai...to aviral --> isme python me routing stuffs dekh lo ek baar routes work karne lage tab hum usko frontend me integrate kare..
 3 isme hamne "main.py" ko nhi touch kia...instead i have done all routing stuffs inside new file "websocket_server.py" to "main.py" work kar rha as it were...aur route work kar rha...uske liye postman ka use kar lena... basss baaki other files me issue aaaye to batana....sab (Amit, Aviral)

<-------------------------------------bass yehi itna batana tha..baaki neeche init ka process hai......enjoyeee--------------------------------------->





# Turborepo starter

This Turborepo starter is maintained by the Turborepo core team.

## Using this example

Run the following command:

```sh
npx create-turbo@latest
```

## What's inside?

This Turborepo includes the following packages/apps:

### Apps and Packages

- `docs`: a [Next.js](https://nextjs.org/) app
- `web`: another [Next.js](https://nextjs.org/) app
- `@repo/ui`: a stub React component library shared by both `web` and `docs` applications
- `@repo/eslint-config`: `eslint` configurations (includes `eslint-config-next` and `eslint-config-prettier`)
- `@repo/typescript-config`: `tsconfig.json`s used throughout the monorepo

Each package/app is 100% [TypeScript](https://www.typescriptlang.org/).

### Utilities

This Turborepo has some additional tools already setup for you:

- [TypeScript](https://www.typescriptlang.org/) for static type checking
- [ESLint](https://eslint.org/) for code linting
- [Prettier](https://prettier.io) for code formatting

### Build

To build all apps and packages, run the following command:

```
cd my-turborepo
pnpm build
```

### Develop

To develop all apps and packages, run the following command:

```
cd my-turborepo
pnpm dev
```


 my-project/
├── .gitignore
├── .npmrc
├── README.md
├── apps/
│   ├── backendd/          
│   │   ├── README.md
│   │   ├── Stampede_detection system
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   ├── stampede_detection_results.csv
│   │   │   ├── stampede_detector.py
│   │   │   └── visualization.py
│   │   ├── stampede_events.log
│   │   └── yolov8n.pt
│   ├── docs/
│   │   ├── .gitignore
│   │   ├── README.md
│   │   ├── app/
│   │   │   ├── fonts/
│   │   │   │   ├── GeistMonoVF.woff
│   │   │   │   └── GeistVF.woff
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   └── page.module.css
│   │   │   └── page.tsx
│   │   ├── eslint.config.js
│   │   ├── next-env.d.ts
│   │   ├── next.config.js
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── frontend/
│   │   ├── .gitignore
│   │   ├── README.md
│   │   ├── app/
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── eslint.config.mjs
│   │   ├── next-env.d.ts
│   │   ├── next.config.ts
│   │   ├── package.json
│   │   ├── pages/
│   │   │   └── index.tsx
│   │   ├── postcss.config.mjs
│   │   ├── public/
│   │   ├── tailwind.config.ts
│   │   └── tsconfig.json
│   └── web/
│       ├── .gitignore
│       ├── README.md
│       ├── app/
│       │   ├── fonts/
│       │   │   ├── GeistMonoVF.woff
│       │   │   └── GeistVF.woff
│       │   ├── globals.css
│       │   ├── layout.tsx
│       │   └── page.module.css
│       │   └── page.tsx
│       ├── eslint.config.js
│       ├── next-env.d.ts
│       ├── next.config.js
│       ├── package.json
│       └── tsconfig.json
├── package.json
├── packages/
│   ├── eslint-config/
│   │   ├── base.js
│   │   ├── next.js
│   │   ├── package.json
│   │   ├── react-internal.js
│   │   └── README.md
│   ├── typescript-config/
│   │   ├── base.json
│   │   ├── nextjs.json
│   │   ├── package.json
│   │   └── react-library.json
│   └── ui/
│       ├── eslint.config.mjs
│       ├── package.json
│       ├── src/
│       │   ├── button.tsx
│       │   ├── card.tsx
│       │   └── code.tsx
│       ├── tsconfig.json
│       └── turbo/
│           ├── generators/
│           │   ├── config.ts
│           │   └── templates/
│           │       └── component.hbs
├── turbo.json
