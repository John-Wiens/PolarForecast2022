import { Routes } from "@angular/router";

import { DashboardComponent } from "../../pages/dashboard/dashboard.component";
import { PredictionsComponent } from "src/app/pages/predictions/predictions.component";
import { MatchesComponent } from "src/app/pages/matches/matches.component";
import { RankingsComponent } from "src/app/pages/rankings/rankings.component";

export const AdminLayoutRoutes: Routes = [
  { path: "dashboard", component: DashboardComponent },
  { path: "rankings", component: RankingsComponent },
  { path: "matches", component: MatchesComponent },
  { path: "predictions", component: PredictionsComponent },
];
