import Layout from "@/components/Layout";
import { createBrowserRouter } from "react-router-dom";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        index: true,
        lazy: async () => {
          const { default: Component } = await import("@/pages/Home");
          return { Component };
        },
      },
      {
        path: "authenticate",
        lazy: async () => {
          const { default: Component } = await import("@/pages/Authenticate");
          return { Component }; 
        }
      },
      {
        path: "units",
        lazy: async () => {
          const { default: Component } = await import("@/pages/Units");
          return { Component };
        },
      },
      {
        path: "items",
        lazy: async () => {
          const { default: Component } = await import("@/pages/Items");
          return { Component };
        },
      },
    //   {
    //     path: "traits",
    //     lazy: async () => {
    //       const { default: Component } = await import("@/pages/Traits");
    //       return { Component };
    //     },
    //   },
    //   {
    //     path: "patch_note",
    //     lazy: async () => {
    //       const { default: Component } = await import("@/pages/PatchNote");
    //       return { Component };
    //     },
    //   },
    //   {
    //     path: "builder",
    //     lazy: async () => {
    //       const { default: Component } = await import("@/pages/Builder");
    //       return { Component };
    //     },
    //   },
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
    //   {
    //     path: "profile",
    //     lazy: async () => {
    //       const { default: Component } = await import("@/pages/SearchProfile");
    //       return { Component };
    //     },
    //   },
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