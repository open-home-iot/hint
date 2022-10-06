import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {GodmodeRoutingModule} from './godmode-routing.module';
import { GodmodeOverviewComponent } from './pages/godmode-overview/godmode-overview.component';
import {GodmodeService} from './godmode.service';
import { GodmodeLatencyTestingComponent } from './godmode-latency-testing/godmode-latency-testing.component';
import { GodmodeHomeSelectionComponent } from './godmode-latency-testing/godmode-home-selection/godmode-home-selection.component';

@NgModule({
  declarations: [
    GodmodeOverviewComponent,
    GodmodeLatencyTestingComponent,
    GodmodeHomeSelectionComponent,
  ],
  imports: [
    GodmodeRoutingModule,
    CommonModule
  ],
  providers: [
    GodmodeService
  ],
})
export class GodmodeModule { }
