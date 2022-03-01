import { Component, OnInit, ViewChild } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';

@Component({
  selector: 'app-rankings',
  templateUrl: './rankings.component.html',
  styleUrls: ['./rankings.component.scss']
})
export class RankingsComponent implements OnInit {

  
  displayedColumns: string[] = ['rank', 'team', 'opr', 'auto','cargo','cargo_count','climb','fouls','power'];
  columnHeaders = ['Rank', 'Team', 'OPR', 'Auto','Cargo','Cargo Count','Climb','Fouls','Power'].slice();
  columnsToDisplay: string[] = this.displayedColumns.slice();
  //displayedColumns: string[] = ['position', 'name', 'weight', 'symbol'];

  data:any = [];
  @ViewChild(MatSort) sort: MatSort;
  
  dataSource = null;

  ngOnInit() {
    this.getRankings();
  }

  constructor(private api: ApiService) { }

  getRankings() {
    const event = this.getEvent();
    if(event!= null){
      this.api.getRankings(event)
      .subscribe(data => {
        if ('rankings' in data){
          this.data = data['rankings'];
          console.log(this.data);
          this.dataSource = new MatTableDataSource(this.data);
          this.dataSource.sort = this.sort;
        }
      });
    }
  }

  getEvent(){
    const event = localStorage.getItem('event');
    if(event == null){
        return "2022week0"
    } else{
        return event;
    }
  }

}
