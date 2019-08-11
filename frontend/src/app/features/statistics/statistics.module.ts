import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// COMPONENTS
import { StatisticsOverviewComponent } from './pages/statistics-overview/statistics-overview.component';

// SERVICES
import { StatisticsService } from './statistics.service';

// MODULES
import { StatisticsRoutingModule } from './statistics-routing.module';
import { StatisticsTrendComponent } from './statistics-trend/statistics-trend.component';

@NgModule({
  declarations: [
    StatisticsOverviewComponent,
    StatisticsTrendComponent
  ],
  imports: [
    StatisticsRoutingModule,
    CommonModule
  ],
  exports: [
    StatisticsOverviewComponent
  ],
  providers: [StatisticsService]
})
export class StatisticsModule {}
