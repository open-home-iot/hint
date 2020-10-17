import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

// COMPONENTS
import { HumeFindComponent } from './hume-find/hume-find.component';

// PAGES
import { HumeOverviewComponent } from './pages/hume-overview/hume-overview.component';

// SERVICES
import { HumeService } from './hume.service';

// MODULES
import { HumeRoutingModule } from './hume-routing.module';

@NgModule({
  declarations: [
    HumeOverviewComponent,
    HumeFindComponent
  ],
  imports: [
    HumeRoutingModule,
    CommonModule,
    ReactiveFormsModule
  ],
  exports: [
    HumeOverviewComponent,
    HumeFindComponent
  ],
  providers: [HumeService]
})
export class HumeModule {}
