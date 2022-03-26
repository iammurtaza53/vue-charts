<template>
  <div class="container-fluid">
    <div class="row">
      <nav class="col-md-2 d-none d-md-block bg-light sidebar">
        <div class="sidebar-sticky">
          <ul class="nav flex-column">
            <li class="nav-item" v-for="ticker in tickers" :key="ticker">
              <a
                class="nav-link"
                href="javascript:void(0)"
                @click="tickerChanged(ticker)"
              >
                {{ ticker }} <span class="sr-only">(current)</span>
              </a>
            </li>
          </ul>
        </div>
      </nav>

      <main role="main" class="col-md-9 ml-sm-auto col-lg-10">
        <h1>{{ ticker}}</h1>
        <div class="d-flex justify-content-between">
          <div class="btn-toolbar mb-2 mb-md-0">
            <div class="btn-group mr-2">
              <div class="custom">
                <label> Select Property: </label>
                <select @change="ChangeProperty">
                  <option value="straddle" selected>Straddle</option>
                  <option value="impliedmove">ImpliedMove</option>
                  <option value="underlying">Underlying</option>
                  <option value="strike">Strike</option>
                  <option value="quarter">Quarter</option>
                </select>
              </div>
              <apexchart
                ref="chart"
                width="800"
                class="custom"
                type="line"
                :options="options"
                :series="series"
              ></apexchart>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";
import axios from "axios";

var data = [];

export default {
  name: "app",
  components: {
    apexchart: VueApexCharts,
  },
  props: ["ticker"],
  data: function () {
    return {
      intervalid1: "",
      id: null,
      existingData: [],
      property: "straddle",
      tickers: [],
      options: {
        chart: {
          id: "vuechart-example",
        },
        xaxis: {
          type: "datetime",
        },
        yaxis: [
          {
            min: (min) => {
              return min;
            },
            max: (max) => {
              return max;
            },
          },
        ],
        tooltip: {
          x: {
            format: "dd MMM yyyy",
          },
        },
      },
      series: [
        {
          name: "straddle",
          data: data,
        },
      ],
    };
  },
  methods: {
    getUniqueTickers() {
      axios.get("http://127.0.0.1:5000/get-unique-tickers").then((res) => {
        this.tickers = res.data;
        this.getAllData();
        this.start();
      });
    },
    getAllData() {
      axios.get("http://127.0.0.1:5000/get-all-changes/" + this.ticker).then((res) => {
        this.existingData = res.data;
        this.renderProperty();
      });
    },
    tickerChanged(ticker) {
      this.$router.push("/" + ticker).then((e) => {
        this.getAllData();
      });
    },
    renderProperty() {
      data = [];
      this.existingData.forEach((element) => {
        let date = new Date(element["dated"]).getTime();
        data.push({
          x: date,
          y: element[this.property],
        });

        this.id = element["changesid"];
      });

      this.$refs.chart.updateSeries([
        {
          data: data,
        },
      ]);
    },
    ChangeProperty(e) {
      this.property = e.target.value;
      this.$refs.chart.updateSeries([
        {
          name: this.property,
        },
      ]);
      this.renderProperty();
    },
    getLatestData() {
      axios.get("http://127.0.0.1:5000/get-last-changes/" + this.ticker).then((res) => {
        let result = res.data;
        if (result.changesid == this.id) {
          return;
        } else {
          this.existingData.push(result);
          this.updateSeries(result);
        }
      });
    },
    updateSeries(result) {
      let date = new Date(result["dated"]).getTime();
      data.push({
        x: date,
        y: result[this.property],
      });
      this.$refs.chart.updateSeries([
        {
          data: data,
        },
      ]);
    },
    start() {
      let that = this;
      this.intervalid1 = setInterval(() => {
        that.getLatestData();
      }, 5000);
    },
  },
  mounted: function () {
    this.getUniqueTickers();
  },
  beforeUnmount() {
    clearInterval(this.intervalid1);
  },
};
</script>

<style></style>
