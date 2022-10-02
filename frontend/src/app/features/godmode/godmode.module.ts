import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {GodmodeRoutingModule} from './godmode-routing.module';
import { GodmodeOverviewComponent } from './pages/godmode-overview/godmode-overview.component';
import { GodmodeHomeFinderComponent } from './godmode-home-finder/godmode-home-finder.component';
import { GodmodeHumeSelectorComponent } from './godmode-hume-selector/godmode-hume-selector.component';
import { GodmodeLatencyTestStartComponent } from './godmode-latency-test-start/godmode-latency-test-start.component';



@NgModule({
  declarations: [
    GodmodeOverviewComponent,
    GodmodeHomeFinderComponent,
    GodmodeHumeSelectorComponent,
    GodmodeLatencyTestStartComponent
  ],
  imports: [
    GodmodeRoutingModule,
    CommonModule
  ]
})
export class GodmodeModule { }
