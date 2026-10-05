import Layout from "@/components/layout";
import { createBrowserRouter } from "react-router-dom";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        index: true,
        lazy: async () => {
          const { default: Component } = await import("@/pages/home");
          return { Component };
        },
      },
      {
        path: "authenticate",
        lazy: async () => {
          const { default: Component } = await import("@/pages/authenticate");
          return { Component }; 
        }
      },
      {
        path: "units",
        lazy: async () => {
          const { default: Component } = await import("@/pages/units");
          return { Component };
        },
      },
      {
        path: "items",
        lazy: async () => {
          const { default: Component } = await import("@/pages/items");
          return { Component };
        },
      },
      {
        path: "traits",
        lazy: async () => {
          const { default: Component } = await import("@/pages/traits");
          return { Component };
        },
      },
      {
        path: "augments",
        lazy: async () => {
          const { default: Component } = await import("@/pages/augments");
          return { Component };
        },
      },
      {
        path: "patch_note",
        lazy: async () => {
          const { default: Component } = await import("@/pages/patchnote");
          return { Component };
        },
      },
      {
        path: "builder",
        lazy: async () => {
          const { default: Component } = await import("@/pages/builder");
          return { Component };
        },
      },
    //   {
    //     path: "meta",
    //     lazy: async () => {
    //       const { default: Component } = await import("@/pages/Meta");
    //       return { Component };
    //     },
    //   },
    //   {
    //     path: "ranking",
    //     lazy: async () => {
    //       const { default: Component } = await import("@/pages/Ranking");
    //       return { Component };
    //     },
    //   },
      {
        path: "profile",
        lazy: async () => {
          const { default: Component } = await import("@/pages/me");
          return { Component };
        },
      },
      {
        path: "users",
        lazy: async () => {
          const { default: Component } = await import("@/pages/user_search");
          return { Component };
        },
      },
      {
        path: "terms",
        lazy: async () => {
          const { default: Component } = await import("@/pages/terms");
          return { Component };
        },
      },
      {
        path: "conditions",
        lazy: async () => {
          const { default: Component } = await import("@/pages/conditions");
          return { Component };
        },
      },
    //   {
    //     path: "profile/*",
    //     lazy: async () => {
    //       const { default: Component } = await import("@/pages/UserProfile");
    //       return { Component };
    //     },
    //   },
    //   {
    //     path: "*",
    //     lazy: async () => {
    //       const { default: Component } = await import("@/pages/NotFound");
    //       return { Component };
    //     },
    //   },
    ],
  },
]);