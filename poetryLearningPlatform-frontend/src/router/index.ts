import { type RouteRecordRaw, createRouter, createWebHashHistory, createWebHistory } from "vue-router"

const Layout = () => import("@/layout/index.vue")

/** 常驻路由 */
export const constantRoutes: RouteRecordRaw[] = [
  {
    path: "/redirect",
    component: Layout,
    meta: {
      hidden: true
    },
    children: [
      {
        path: "/redirect/:path(.*)",
        component: () => import("@/views/redirect/index.vue")
      }
    ]
  },
  {
    path: "/403",
    component: () => import("@/views/error-page/403.vue"),
    meta: {
      hidden: true
    }
  },
  {
    path: "/404",
    component: () => import("@/views/error-page/404.vue"),
    meta: {
      hidden: true
    },
    alias: "/:pathMatch(.*)*"
  },
  {
    path: "/login",
    component: () => import("@/views/login/index.vue"),
    meta: {
      hidden: true
    }
  },
  {
    path: "/poem/cloud/:query_method/:query_id",
    component: Layout,
    meta: {
      hidden: true
    },
    children: [
      {
        path: "",
        component: () => import("@/views/poem/PoemCloud.vue"),
        meta: {
          hidden: true
        },
        props: true
      }
    ]
  },
  {
    path: "/poem/search_poem_list/:query_method/:query_text",
    component: Layout,
    meta: {
      hidden: true
    },
    children: [
      {
        path: "",
        component: () => import("@/views/poem/PoemSearchList.vue"),
        meta: {
          hidden: true
        },
        props: true
      }
    ]
  },
  {
    path: "/author",
    component: Layout,
    meta: {
      hidden: true
    },
    children: [
      {
        path: "author",
        component: () => import("@/views/poem/Author.vue"),
        meta: {
          hidden: true
        },
        props: true
      }
    ]
  },
  {
    path: "/collection",
    component: Layout,
    meta: {
      hidden: true
    },
    children: [
      {
        path: "collection",
        component: () => import("@/views/poem/Collection.vue"),
        meta: {
          hidden: true
        },
        props: true
      }
    ]
  },
  {
    path: "/rhythmic",
    component: Layout,
    meta: {
      hidden: true
    },
    children: [
      {
        path: "rhythmic",
        component: () => import("@/views/poem/Rhythmic.vue"),
        meta: {
          hidden: true
        },
        props: true
      }
    ]
  },
  {
    path: "/search_poem_other_list/:query_method/:query_text",
    component: Layout,
    meta: {
      hidden: true
    },
    children: [
      {
        path: "",
        component: () => import("@/views/poem/PoemSearchByOther.vue"),
        props: true
      }
    ]
  },
  {
    path: "/poem/:poem_id",
    component: Layout,
    meta: {
      hidden: true
    },
    children: [
      {
        path: "",
        component: () => import("../components/Poem.vue"),
        props: true
      }
    ]
  },
  {
    path: "/register",
    component: () => import("@/views/register/index.vue"),
    meta: {
      hidden: true
    }
  },
  {
    path: "/",
    component: Layout,
    redirect: "/dashboard",
    children: [
      {
        path: "",
        component: () => import("@/views/dashboard/Home.vue"),
        name: "Dashboard",
        meta: {
          title: "首页",
          svgIcon: "dashboard",
          affix: true
        }
      }
    ]
  },
  {
    path: "/",
    component: Layout,
    redirect: "/learn",
    children: [
      {
        path: "learn",
        component: () => import("@/views/learn/index.vue"),
        name: "Learn",
        meta: {
          title: "问答学习",
          svgIcon: "shici",
          affix: true
        }
      }
    ]
  },
  {
    path: "/search-menu",
    component: Layout,
    redirect: "/search-menu/search",
    name: "SearchMenu",
    meta: {
      title: "诗词搜索",
      elIcon: "menu"
    },
    children: [
      {
        path: "search",
        component: () => import("@/views/search-menu/search/index.vue"),
        name: "Search",
        meta: {
          title: "搜索",
          svgIcon: "搜索"
        }
      },
      {
        path: "author",
        component: () => import("@/views/search-menu/author/index.vue"),
        name: "Author",
        meta: {
          title: "诗人",
          svgIcon: "诗人"
        }
      },
      {
        path: "rhythmic",
        component: () => import("@/views/search-menu/rhythmic/index.vue"),
        name: "Rhythmic",
        meta: {
          title: "词牌/韵律",
          svgIcon: "韵律"
        }
      },
      {
        path: "collection",
        component: () => import("@/views/search-menu/collection/index.vue"),
        name: "Collection",
        meta: {
          title: "诗集",
          svgIcon: "诗集"
        }
      }
    ]
  },
  {
    path: "/menu",
    component: Layout,
    redirect: "/menu/menu1",
    name: "Menu",
    meta: {
      title: "敬请期待",
      svgIcon: "menu"
    },
    children: [
      {
        path: "menu1",
        component: () => import("@/views/menu/menu1/index.vue"),
        redirect: "/menu/menu1/menu1-1",
        name: "Menu1",
        meta: {
          title: "menu1"
        },
        children: [
          {
            path: "menu1-1",
            component: () => import("@/views/menu/menu1/menu1-1/index.vue"),
            name: "Menu1-1",
            meta: {
              title: "menu1-1"
            }
          },
          {
            path: "menu1-2",
            component: () => import("@/views/menu/menu1/menu1-2/index.vue"),
            redirect: "/menu/menu1/menu1-2/menu1-2-1",
            name: "Menu1-2",
            meta: {
              title: "menu1-2"
            },
            children: [
              {
                path: "menu1-2-1",
                component: () => import("@/views/menu/menu1/menu1-2/menu1-2-1/index.vue"),
                name: "Menu1-2-1",
                meta: {
                  title: "menu1-2-1"
                }
              },
              {
                path: "menu1-2-2",
                component: () => import("@/views/menu/menu1/menu1-2/menu1-2-2/index.vue"),
                name: "Menu1-2-2",
                meta: {
                  title: "menu1-2-2"
                }
              }
            ]
          },
          {
            path: "menu1-3",
            component: () => import("@/views/menu/menu1/menu1-3/index.vue"),
            name: "Menu1-3",
            meta: {
              title: "menu1-3"
            }
          }
        ]
      },
      {
        path: "menu2",
        component: () => import("@/views/menu/menu2/index.vue"),
        name: "Menu2",
        meta: {
          title: "menu2"
        }
      }
    ]
  }
]

/**
 * 动态路由
 * 用来放置有权限 (Roles 属性) 的路由
 * 必须带有 Name 属性
 */
export const asyncRoutes: RouteRecordRaw[] = [
  {
    path: "/",
    component: Layout,
    meta: {
      roles: ["admin"]
    },
    children: [
      {
        path: "user-manage",
        component: () => import("@/views/user-manage/index.vue"),
        name: "UserManage",
        meta: {
          title: "用户管理",
          elIcon: "Grid"
        }
      }
    ]
  },
  {
    path: "/permission",
    component: Layout,
    redirect: "/permission/page",
    name: "Permission",
    meta: {
      roles: ["admin"] // 可以在根路由中设置角色
      // alwaysShow: true // 将始终显示根菜单
    },
    children: [
      {
        path: "page",
        component: () => import("@/views/permission/page.vue"),
        name: "PagePermission",
        meta: {
          title: "切换权限",
          svgIcon: "lock"
        }
      }
      // {
      //   path: "directive",
      //   component: () => import("@/views/permission/directive.vue"),
      //   name: "DirectivePermission",
      //   meta: {
      //     title: "指令权限" // 如果未设置角色，则表示：该页面不需要权限，但会继承根路由的角色
      //   }
      // }
    ]
  },
  // {
  //   path: "/permission",
  //   component: Layout,
  //   redirect: "/permission/page",
  //   name: "Permission",
  //   meta: {
  //     title: "权限管理",
  //     svgIcon: "lock",
  //     roles: ["admin", "user"], // 可以在根路由中设置角色
  //     alwaysShow: true // 将始终显示根菜单
  //   },
  //   children: [
  //     {
  //       path: "page",
  //       component: () => import("@/views/permission/page.vue"),
  //       name: "PagePermission",
  //       meta: {
  //         title: "页面权限",
  //         roles: ["admin"] // 或者在子导航中设置角色
  //       }
  //     },
  //     {
  //       path: "directive",
  //       component: () => import("@/views/permission/directive.vue"),
  //       name: "DirectivePermission",
  //       meta: {
  //         title: "指令权限" // 如果未设置角色，则表示：该页面不需要权限，但会继承根路由的角色
  //       }
  //     }
  //   ]
  // },
  {
    path: "/:pathMatch(.*)*", // Must put the 'ErrorPage' route at the end, 必须将 'ErrorPage' 路由放在最后
    redirect: "/404",
    name: "ErrorPage",
    meta: {
      hidden: true
    }
  }
]

const router = createRouter({
  history:
    import.meta.env.VITE_ROUTER_HISTORY === "hash"
      ? createWebHashHistory(import.meta.env.VITE_PUBLIC_PATH)
      : createWebHistory(import.meta.env.VITE_PUBLIC_PATH),
  routes: constantRoutes
})

/** 重置路由 */
export function resetRouter() {
  // 注意：所有动态路由路由必须带有 Name 属性，否则可能会不能完全重置干净
  try {
    router.getRoutes().forEach((route) => {
      const { name, meta } = route
      if (name && meta.roles?.length) {
        router.hasRoute(name) && router.removeRoute(name)
      }
    })
  } catch (error) {
    // 强制刷新浏览器也行，只是交互体验不是很好
    window.location.reload()
  }
}

export default router
