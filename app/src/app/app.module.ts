import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { NgModule } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { HttpClientModule } from "@angular/common/http";
import { RouterModule } from "@angular/router";
import { ToastrModule } from 'ngx-toastr';
import { AppComponent } from "./app.component";
import { AdminLayoutComponent } from "./layouts/admin-layout/admin-layout.component";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";
import { AppRoutingModule } from "./app-routing.module";
import { ComponentsModule } from "./components/components.module";
import { RankingsComponent } from './pages/rankings/rankings.component';
import { MatchesComponent } from './pages/matches/matches.component';
import { PredictionsComponent } from './pages/predictions/predictions.component';
import { MatTableModule} from '@angular/material/table';
import { MatSortModule, MatSort} from '@angular/material/sort';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatExpansionModule } from '@angular/material/expansion';

@NgModule({
  imports: [
    BrowserAnimationsModule,
    FormsModule,
    HttpClientModule,
    ComponentsModule,
    NgbModule,
    RouterModule,
    AppRoutingModule,
    MatTableModule,
    MatSortModule,
    MatAutocompleteModule,
    MatExpansionModule,
    ToastrModule.forRoot()
  ],
  declarations: [AppComponent, AdminLayoutComponent],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
