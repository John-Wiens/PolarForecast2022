import { Component, OnInit } from "@angular/core";

declare interface RouteInfo {
  path: string;
  title: string;
  rtlTitle: string;
  icon: string;
  class: string;
}
export const ROUTES: RouteInfo[] = [
  {
    path: "/dashboard",
    title: "Dashboard",
    rtlTitle: "",
    icon: "icon-chart-pie-36",
    class: ""
  },
  {
    path: "/tables",
    title: "Table List",
    rtlTitle: "",
    icon: "icon-puzzle-10",
    class: ""
  },
  {
    path: "/rankings",
    title: "Rankings",
    rtlTitle: "",
    icon: "icon-puzzle-10",
    class: ""
  },
  {
    path: "/matches",
    title: "Matches",
    rtlTitle: "",
    icon: "icon-puzzle-10",
    class: ""
  },
  {
    path: "/predictions",
    title: "Predictions",
    rtlTitle: "",
    icon: "icon-puzzle-10",
    class: ""
  },
];

@Component({
  selector: "app-sidebar",
  templateUrl: "./sidebar.component.html",
  styleUrls: ["./sidebar.component.css"]
})
export class SidebarComponent implements OnInit {
  menuItems: any[];

  constructor() {}

  ngOnInit() {
    this.menuItems = ROUTES.filter(menuItem => menuItem);
  }
  isMobileMenu() {
    if (window.innerWidth > 991) {
      return false;
    }
    return true;
  }
}
