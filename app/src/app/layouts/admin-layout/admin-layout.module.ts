import { NgModule } from "@angular/core";
import { HttpClientModule } from "@angular/common/http";
import { RouterModule } from "@angular/router";
import { CommonModule } from "@angular/common";

import { AdminLayoutRoutes } from "./admin-layout.routing";
import { DashboardComponent } from "../../pages/dashboard/dashboard.component";
// import { RtlComponent } from "../../pages/rtl/rtl.component";

import { NgbModule } from "@ng-bootstrap/ng-bootstrap";
import { MatchesComponent } from "src/app/pages/matches/matches.component";
import { RankingsComponent } from "src/app/pages/rankings/rankings.component";
import { PredictionsComponent } from "src/app/pages/predictions/predictions.component";
import { MatTableModule} from '@angular/material/table';
import { MatSortModule, MatSort} from '@angular/material/sort';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatExpansionModule } from '@angular/material/expansion';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';

@NgModule({
  imports: [
    CommonModule,
    MatTableModule,
    MatSortModule,
    MatAutocompleteModule,
    MatExpansionModule,
    MatFormFieldModule,
    MatInputModule,
    RouterModule.forChild(AdminLayoutRoutes),
    FormsModule,
    HttpClientModule,
    NgbModule,
    FormsModule,
    ReactiveFormsModule,
    MatSelectModule,
    
  ],
  declarations: [
    DashboardComponent,
    RankingsComponent,
    MatchesComponent,
    PredictionsComponent
  ]
})
export class AdminLayoutModule {}
