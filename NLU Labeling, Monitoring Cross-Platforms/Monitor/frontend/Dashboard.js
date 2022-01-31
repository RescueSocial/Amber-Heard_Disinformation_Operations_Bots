import React, { Component } from 'react';
import { Bar, Line } from 'react-chartjs-2';

import {
	// Badge,
	Button,
	ButtonDropdown,
	ButtonGroup,
	ButtonToolbar,
	Card,
	CardBody,
	CardFooter,
	CardHeader,
	CardTitle,
	Col,
	Dropdown,
	DropdownItem,
	DropdownMenu,
	DropdownToggle,
	Progress,
	Row,
	Table,
} from 'reactstrap';
import { CustomTooltips } from '@coreui/coreui-plugin-chartjs-custom-tooltips';
import {
	getStyle,
	hexToRgba,
} from '@coreui/coreui-pro/dist/js/coreui-utilities';

// Services
import { DashboardService } from '../../services/dashboard/dashboardService';

// const Widget03 = lazy(() => import('../../views/Widgets/Widget03'));

const brandPrimary = getStyle('--primary');
const brandSuccess = getStyle('--success');
const brandInfo = getStyle('--info');
// const brandWarning = getStyle('--warning')
const brandDanger = getStyle('--danger');

// Card Chart 1
const cardChartData1 = {
	labels: ['4/3', '4/4', '4/5', '4/6', '4/7', '4/8', '4/9'],
	datasets: [
		{
			label: 'The total count of users who tweet for Amber Heard',
			backgroundColor: brandPrimary,
			borderColor: 'rgba(255,255,255,.55)',
			data: [65, 59, 84, 84, 51, 55, 40],
		},
	],
};

const cardChartOpts1 = {
	tooltips: {
		enabled: false,
		custom: CustomTooltips,
	},
	maintainAspectRatio: false,
	legend: {
		display: false,
	},
	scales: {
		xAxes: [
			{
				gridLines: {
					color: 'transparent',
					zeroLineColor: 'transparent',
				},
				ticks: {
					fontSize: 2,
					fontColor: 'transparent',
				},
			},
		],
		yAxes: [
			{
				display: false,
				ticks: {
					display: false,
					min: Math.min.apply(Math, cardChartData1.datasets[0].data) - 5,
					max: Math.max.apply(Math, cardChartData1.datasets[0].data) + 5,
				},
			},
		],
	},
	elements: {
		line: {
			borderWidth: 1,
		},
		point: {
			radius: 4,
			hitRadius: 10,
			hoverRadius: 4,
		},
	},
};

// Card Chart 2
const cardChartData2 = {
	labels: ['4/3', '4/4', '4/5', '4/6', '4/7', '4/8', '4/9'],
	datasets: [
		{
			label: 'The count of users who support for Amber Heard',
			backgroundColor: brandInfo,
			borderColor: 'rgba(255,255,255,.55)',
			data: [1, 18, 9, 17, 34, 22, 11],
		},
	],
};

const cardChartOpts2 = {
	tooltips: {
		enabled: false,
		custom: CustomTooltips,
	},
	maintainAspectRatio: false,
	legend: {
		display: false,
	},
	scales: {
		xAxes: [
			{
				gridLines: {
					color: 'transparent',
					zeroLineColor: 'transparent',
				},
				ticks: {
					fontSize: 2,
					fontColor: 'transparent',
				},
			},
		],
		yAxes: [
			{
				display: false,
				ticks: {
					display: false,
					min: Math.min.apply(Math, cardChartData2.datasets[0].data) - 5,
					max: Math.max.apply(Math, cardChartData2.datasets[0].data) + 5,
				},
			},
		],
	},
	elements: {
		line: {
			tension: 0.00001,
			borderWidth: 1,
		},
		point: {
			radius: 4,
			hitRadius: 10,
			hoverRadius: 4,
		},
	},
};

// Card Chart 3
const cardChartData3 = {
	labels: ['4/3', '4/4', '4/5', '4/6', '4/7', '4/8', '4/9'],
	datasets: [
		{
			label: 'The count of users who offense for Amber Heard',
			backgroundColor: 'rgba(255,255,255,.2)',
			borderColor: 'rgba(255,255,255,.55)',
			data: [78, 81, 80, 45, 34, 12, 40],
		},
	],
};

const cardChartOpts3 = {
	tooltips: {
		enabled: false,
		custom: CustomTooltips,
	},
	maintainAspectRatio: false,
	legend: {
		display: false,
	},
	scales: {
		xAxes: [
			{
				display: false,
			},
		],
		yAxes: [
			{
				display: false,
			},
		],
	},
	elements: {
		line: {
			borderWidth: 2,
		},
		point: {
			radius: 0,
			hitRadius: 10,
			hoverRadius: 4,
		},
	},
};

// Card Chart 4
const cardChartData4 = {
	labels: ['4/3', '4/4', '4/5', '4/6', '4/7', '4/8', '4/9'],
	datasets: [
		{
			label: 'The count of users who be unbiased for Amber Heard',
			backgroundColor: 'rgba(255,255,255,.3)',
			borderColor: 'transparent',
			data: [78, 81, 80, 45, 34, 12, 40],
		},
	],
};

const cardChartOpts4 = {
	tooltips: {
		enabled: false,
		custom: CustomTooltips,
	},
	maintainAspectRatio: false,
	legend: {
		display: false,
	},
	scales: {
		xAxes: [
			{
				display: false,
				barPercentage: 0.6,
			},
		],
		yAxes: [
			{
				display: false,
			},
		],
	},
};

//Random Numbers
function random(min, max) {
	return Math.floor(Math.random() * (max - min + 1) + min);
}

var elements = 27;
var data1 = [];
var data2 = [];
var data3 = [];

for (var i = 0; i <= elements; i++) {
	data1.push(random(10, 200) + i * 4);
	data2.push(random(70, 150));
	data3.push(random(80, 100));
}

class Dashboard extends Component {
	constructor(props) {
		super(props);

		this.apiService = new DashboardService();

		this.state = {
			loading: true,
			data1: [],
			data2: [],
			data3: [],
			test: [],
			mainChartLabels: [],
			total_tweets: 0,
			support_tweets: 0,
			offense_tweets: 0,
			unbiased_tweets: 0,
			support_rate: 0,
			dropdownOpen: false,
			radioSelected: 2,
			defaultHeight: 300,
			mainChartOption: {},
		};

		this.toggle = this.toggle.bind(this);
		this.onRadioBtnClick = this.onRadioBtnClick.bind(this);
		// this.getUnbiasedTweets = this.getUnbiasedTweets.bind(this);
	}

	componentDidMount() {
		this.fetchData();
		this.interval = setInterval(() => this.fetchData(), 5000);
	}
	componentWillUnmount() {
		clearInterval(this.interval);
	}
	// Fetch Dashboard Data and Set State
	fetchData = async () => {
		this.setState((prev) => ({ ...prev, loading: true }));
		try {
			// debugger;
			const url = '';
			//   debugger;
			const response = await this.apiService.fetchAll(url);
			this.setState((prev) => ({
				...prev,
				all_users: response.users[0],
				support_users: response.users[1],
				offense_users: response.users[2],
				none_users: response.users[3],
				total_tweets: response.total_tweets[0],
				support_tweets: response.total_tweets[1],
				offense_tweets: response.total_tweets[2],
				unbiased_tweets:
					response.total_tweets[0] -
					response.total_tweets[1] -
					response.total_tweets[2],
				support_rate:
					Math.round(
						(response.total_tweets[1] * 10000) /
							(response.total_tweets[1] + response.total_tweets[2])
					) / 100,
				mainChartLabels: response.tweets.labels,
				data1: response.tweets.datas[0],
				data2: response.tweets.datas[1],
				data3: response.tweets.datas[2],
				mainChartOption: this.setMainChartOps(response.tweets.datas),
			}));
			console.log(response);
		} catch (error) {
			console.log(error);
		}
	};
	showMainChart() {
		return {
			labels: this.state.mainChartLabels,
			datasets: [
				{
					label: 'Support Tweets',
					backgroundColor: hexToRgba(brandSuccess, 10),
					borderColor: brandSuccess,
					pointHoverBackgroundColor: '#fff',
					borderWidth: 3,
					data: this.state.data1,
				},
				{
					label: 'Offense Tweets',
					backgroundColor: 'transparent',
					borderColor: brandDanger,
					pointHoverBackgroundColor: '#fff',
					borderWidth: 2,
					data: this.state.data2,
				},
				{
					label: 'Neutral Tweets',
					backgroundColor: hexToRgba(brandInfo, 10),
					borderColor: brandInfo,
					pointHoverBackgroundColor: '#fff',
					borderWidth: 2,
					borderDash: [8, 5],
					data: this.state.data3,
				},
			],
		};
	}

	setMainChartOps(datas) {
		console.log('here');
    // debugger;
		const maximum = Math.max(...datas[0], ...datas[1], ...datas[2]);
		const height = Math.ceil(maximum);
		this.setState((prev) => ({ ...prev, defaultHeight: height }));
		return {
			tooltips: {
				enabled: false,
				custom: CustomTooltips,
				intersect: true,
				mode: 'index',
				position: 'nearest',
				callbacks: {
					labelColor: function (tooltipItem, chart) {
						return {
							backgroundColor:
								chart.data.datasets[tooltipItem.datasetIndex].borderColor,
						};
					},
				},
			},
			maintainAspectRatio: false,
			legend: {
				display: false,
			},
			scales: {
				xAxes: [
					{
						gridLines: {
							drawOnChartArea: false,
						},
					},
				],
				yAxes: [
					{
						ticks: {
							beginAtZero: true,
							maxTicksLimit: 5,
							stepSize: Math.ceil(height / 5),
							max: height,
						},
					},
				],
			},
			elements: {
				point: {
					radius: 0,
					hitRadius: 10,
					hoverRadius: 4,
					hoverBorderWidth: 3,
				},
			},
		};
	}
	toggle() {
		this.setState({
			dropdownOpen: !this.state.dropdownOpen,
		});
	}

	onRadioBtnClick(radioSelected) {
		this.setState({
			radioSelected: radioSelected,
		});
	}

	loading = () => (
		<div className="animated fadeIn pt-1 text-center">Loading...</div>
	);

	render() {
		return (
			<div className="animated fadeIn">
				<Row>
					<Col xs="12" sm="6" lg="3">
						<Card className="text-white bg-info">
							<CardBody className="pb-0">
								<ButtonGroup className="float-right">
									<ButtonDropdown
										id="card1"
										isOpen={this.state.card1}
										toggle={() => {
											this.setState({ card1: !this.state.card1 });
										}}
									>
										<DropdownToggle caret className="p-0" color="transparent">
											<i className="icon-settings"></i>
										</DropdownToggle>
										<DropdownMenu right>
											<DropdownItem>Week</DropdownItem>
											<DropdownItem>Month</DropdownItem>
											<DropdownItem>Year</DropdownItem>
										</DropdownMenu>
									</ButtonDropdown>
								</ButtonGroup>
								<div className="text-value">{this.state.all_users}</div>
								<div>Total Users</div>
								<div className="chart-wrapper mt-3" style={{ height: '70px' }}>
									<Line
										data={cardChartData2}
										options={cardChartOpts2}
										height={70}
									/>
								</div>
							</CardBody>
						</Card>
					</Col>

					<Col xs="12" sm="6" lg="3">
						<Card className="text-white bg-primary">
							<CardBody className="pb-0">
								<ButtonGroup className="float-right">
									<Dropdown
										id="card2"
										isOpen={this.state.card2}
										toggle={() => {
											this.setState({ card2: !this.state.card2 });
										}}
									>
										<DropdownToggle className="p-0" color="transparent">
											<i className="icon-location-pin"></i>
										</DropdownToggle>
										<DropdownMenu right>
											<DropdownItem>Week</DropdownItem>
											<DropdownItem>Month</DropdownItem>
											<DropdownItem>Year</DropdownItem>
										</DropdownMenu>
									</Dropdown>
								</ButtonGroup>
								<div className="text-value">{this.state.support_users}</div>
								<div>Support Users</div>
								<div className="chart-wrapper mt-3" style={{ height: '70px' }}>
									<Line
										data={cardChartData1}
										options={cardChartOpts1}
										height={70}
									/>
								</div>
							</CardBody>
						</Card>
					</Col>

					<Col xs="12" sm="6" lg="3">
						<Card className="text-white bg-danger">
							<CardBody className="pb-0">
								<ButtonGroup className="float-right">
									<Dropdown
										id="card3"
										isOpen={this.state.card3}
										toggle={() => {
											this.setState({ card3: !this.state.card3 });
										}}
									>
										<DropdownToggle caret className="p-0" color="transparent">
											<i className="icon-settings"></i>
										</DropdownToggle>
										<DropdownMenu right>
											<DropdownItem>Week</DropdownItem>
											<DropdownItem>Month</DropdownItem>
											<DropdownItem>Year</DropdownItem>
										</DropdownMenu>
									</Dropdown>
								</ButtonGroup>
								<div className="text-value">{this.state.offense_users}</div>
								<div>Offense Users</div>
							</CardBody>
							<div className="chart-wrapper mt-3" style={{ height: '70px' }}>
								<Line
									data={cardChartData3}
									options={cardChartOpts3}
									height={70}
								/>
							</div>
						</Card>
					</Col>

					<Col xs="12" sm="6" lg="3">
						<Card className="text-white bg-warning">
							<CardBody className="pb-0">
								<ButtonGroup className="float-right">
									<ButtonDropdown
										id="card4"
										isOpen={this.state.card4}
										toggle={() => {
											this.setState({ card4: !this.state.card4 });
										}}
									>
										<DropdownToggle caret className="p-0" color="transparent">
											<i className="icon-settings"></i>
										</DropdownToggle>
										<DropdownMenu right>
											<DropdownItem>Week</DropdownItem>
											<DropdownItem>Month</DropdownItem>
											<DropdownItem>Year</DropdownItem>
										</DropdownMenu>
									</ButtonDropdown>
								</ButtonGroup>
								<div className="text-value">{this.state.none_users}</div>
								<div>Neutral Users</div>
							</CardBody>
							<div
								className="chart-wrapper mt-3 mx-3"
								style={{ height: '70px' }}
							>
								<Bar
									data={cardChartData4}
									options={cardChartOpts4}
									height={70}
								/>
							</div>
						</Card>
					</Col>
				</Row>
				<Row>
					<Col>
						<Card>
							<CardBody>
								<Row>
									<Col sm="5">
										<CardTitle className="mb-0">
											Tweets Trend for Amber Heard
										</CardTitle>
										<div className="small text-muted">March 2021</div>
									</Col>
									<Col sm="7" className="d-none d-sm-inline-block">
										<Button color="primary" className="float-right">
											<i className="icon-cloud-download"></i>
										</Button>
										<ButtonToolbar
											className="float-right"
											aria-label="Toolbar with button groups"
										>
											<ButtonGroup className="mr-3" aria-label="First group">
												<Button
													color="outline-secondary"
													onClick={() => this.onRadioBtnClick(1)}
													active={this.state.radioSelected === 1}
												>
													Day
												</Button>
												<Button
													color="outline-secondary"
													onClick={() => this.onRadioBtnClick(2)}
													active={this.state.radioSelected === 2}
												>
													Month
												</Button>
												<Button
													color="outline-secondary"
													onClick={() => this.onRadioBtnClick(3)}
													active={this.state.radioSelected === 3}
												>
													Year
												</Button>
											</ButtonGroup>
										</ButtonToolbar>
									</Col>
								</Row>
								<div
									className="chart-wrapper"
									style={{
										height: 300 + 'px',
										marginTop: 40 + 'px',
									}}
								>
									<Line
										data={this.showMainChart.bind(this)}
										options={this.mainChartOption}
										height={60}
									/>
								</div>
							</CardBody>
							<CardFooter>
								<Row className="text-center">
									<Col sm={12} md className="mb-sm-2 mb-0">
										<div className="text-muted">Total Tweets</div>
										<strong>{this.state.total_tweets} Tweets (100%)</strong>
										<Progress
											className="progress-xs mt-2"
											color="success"
											value="100"
										/>
									</Col>
									<Col sm={12} md className="mb-sm-2 mb-0 d-md-down-none">
										<div className="text-muted">Support Tweets</div>
										<strong>
											{this.state.support_tweets} Tweets (
											{Math.round(
												(this.state.support_tweets * 10000) /
													this.state.total_tweets
											) / 100}
											%)
										</strong>
										<Progress
											className="progress-xs mt-2"
											color="info"
											value={
												Math.round(
													(this.state.support_tweets * 10000) /
														this.state.total_tweets
												) / 100
											}
										/>
									</Col>
									<Col sm={12} md className="mb-sm-2 mb-0">
										<div className="text-muted">Offense Tweets</div>
										<strong>
											{this.state.offense_tweets} Tweets (
											{Math.round(
												(this.state.offense_tweets * 10000) /
													this.state.total_tweets
											) / 100}
											%)
										</strong>
										<Progress
											className="progress-xs mt-2"
											color="danger"
											value={
												Math.round(
													(this.state.offense_tweets * 10000) /
														this.state.total_tweets
												) / 100
											}
										/>
									</Col>
									<Col sm={12} md className="mb-sm-2 mb-0">
										<div className="text-muted">Neutral Tweets</div>
										<strong>
											{this.state.unbiased_tweets} Tweets (
											{(
												(this.state.unbiased_tweets * 100) /
												this.state.total_tweets
											).toFixed(2)}
											%)
										</strong>
										<Progress
											className="progress-xs mt-2"
											color="warning"
											value={(
												(this.state.unbiased_tweets * 100) /
												this.state.total_tweets
											).toFixed(2)}
										/>
									</Col>
									<Col sm={12} md className="mb-sm-2 mb-0 d-md-down-none">
										<div className="text-muted">Support Rate vs Offense</div>
										<strong>
											Average Support Rate ({this.state.support_rate}%)
										</strong>
										<Progress
											className="progress-xs mt-2"
											color="primary"
											value={this.state.support_rate}
										/>
									</Col>
								</Row>
							</CardFooter>
						</Card>
					</Col>
				</Row>

				<Row>
					<Col>
						<Card>
							<CardHeader>Users</CardHeader>
							<CardBody>
								<Table
									hover
									responsive
									className="table-outline mb-0 d-none d-sm-table"
								>
									<thead className="thead-light">
										<tr>
											<th className="text-center">
												<i className="icon-people"></i>
											</th>
											<th>User</th>
											<th className="text-center">Country</th>
											<th>Tweets</th>
											<th className="text-center">Social Site</th>
											<th>Final Activity</th>
										</tr>
									</thead>
									<tbody>
										<tr>
											<td className="text-center">
												<div className="avatar">
													<img
														src={'assets/img/avatars/1.jpg'}
														className="img-avatar"
														alt="admin@bootstrapmaster.com"
													/>
													<span className="avatar-status badge-success"></span>
												</div>
											</td>
											<td>
												<div>Yiorgos Avraamu</div>
												<div className="small text-muted">
													<span>Support</span> | Registered: Jan 1, 2020
												</div>
											</td>
											<td className="text-center">
												<i
													className="flag-icon flag-icon-us h4 mb-0"
													title="us"
													id="us"
												></i>
											</td>
											<td>
												<div className="clearfix">
													<div className="float-left">
														<strong>1000 tweets, 80% support</strong>
													</div>
													<div className="float-right">
														<small className="text-muted">
															Jun 11, 2020 - Jul 10, 2020
														</small>
													</div>
												</div>
												<Progress
													className="progress-xs"
													color="success"
													value="80"
												/>
											</td>
											<td className="text-center">
												<strong>Twitter</strong>
											</td>
											<td>
												<div className="small text-muted">Last Tweet</div>
												<strong>10 sec ago</strong>
											</td>
										</tr>
										<tr>
											<td className="text-center">
												<div className="avatar">
													<img
														src={'assets/img/avatars/2.jpg'}
														className="img-avatar"
														alt="admin@bootstrapmaster.com"
													/>
													<span className="avatar-status badge-warning"></span>
												</div>
											</td>
											<td>
												<div>Avram Tarasios</div>
												<div className="small text-muted">
													<span>Neutral</span> | Registered: Jan 1, 2020
												</div>
											</td>
											<td className="text-center">
												<i
													className="flag-icon flag-icon-br h4 mb-0"
													title="br"
													id="br"
												></i>
											</td>
											<td>
												<div className="clearfix">
													<div className="float-left">
														<strong>1000 Tweets, 60% Neutral</strong>
													</div>
													<div className="float-right">
														<small className="text-muted">
															Jun 11, 2020 - Jul 10, 2020
														</small>
													</div>
												</div>
												<Progress
													className="progress-xs"
													color="warning"
													value="60"
												/>
											</td>
											<td className="text-center">
												<strong>Twitter</strong>
											</td>
											<td>
												<div className="small text-muted">Last Tweet</div>
												<strong>5 minutes ago</strong>
											</td>
										</tr>
										<tr>
											<td className="text-center">
												<div className="avatar">
													<img
														src={'assets/img/avatars/3.jpg'}
														className="img-avatar"
														alt="admin@bootstrapmaster.com"
													/>
													<span className="avatar-status badge-danger"></span>
												</div>
											</td>
											<td>
												<div>Quintin Ed</div>
												<div className="small text-muted">
													<span>Offense</span> | Registered: Jan 1, 2020
												</div>
											</td>
											<td className="text-center">
												<i
													className="flag-icon flag-icon-in h4 mb-0"
													title="in"
													id="in"
												></i>
											</td>
											<td>
												<div className="clearfix">
													<div className="float-left">
														<strong>1000 Tweets, 74% Offense</strong>
													</div>
													<div className="float-right">
														<small className="text-muted">
															Jun 11, 2020 - Jul 10, 2020
														</small>
													</div>
												</div>
												<Progress
													className="progress-xs"
													color="danger"
													value="74"
												/>
											</td>
											<td className="text-center">
												<strong>Twitter</strong>
											</td>
											<td>
												<div className="small text-muted">Last Tweet</div>
												<strong>1 hour ago</strong>
											</td>
										</tr>
										<tr>
											<td className="text-center">
												<div className="avatar">
													<img
														src={'assets/img/avatars/4.jpg'}
														className="img-avatar"
														alt="admin@bootstrapmaster.com"
													/>
													<span className="avatar-status badge-success"></span>
												</div>
											</td>
											<td>
												<div>Enéas Kwadwo</div>
												<div className="small text-muted">
													<span>Support</span> | Registered: Jan 1, 2020
												</div>
											</td>
											<td className="text-center">
												<i
													className="flag-icon flag-icon-fr h4 mb-0"
													title="fr"
													id="fr"
												></i>
											</td>
											<td>
												<div className="clearfix">
													<div className="float-left">
														<strong>1234 tweets, 85% support</strong>
													</div>
													<div className="float-right">
														<small className="text-muted">
															Jun 11, 2020 - Jul 10, 2020
														</small>
													</div>
												</div>
												<Progress
													className="progress-xs"
													color="success"
													value="85"
												/>
											</td>
											<td className="text-center">
												<strong>Twitter</strong>
											</td>
											<td>
												<div className="small text-muted">Last Tweet</div>
												<strong>Last month</strong>
											</td>
										</tr>
										<tr>
											<td className="text-center">
												<div className="avatar">
													<img
														src={'assets/img/avatars/5.jpg'}
														className="img-avatar"
														alt="admin@bootstrapmaster.com"
													/>
													<span className="avatar-status badge-danger"></span>
												</div>
											</td>
											<td>
												<div>Agapetus Tadeáš</div>
												<div className="small text-muted">
													<span>Offense</span> | Registered: Jan 1, 2021
												</div>
											</td>
											<td className="text-center">
												<i
													className="flag-icon flag-icon-es h4 mb-0"
													title="es"
													id="es"
												></i>
											</td>
											<td>
												<div className="clearfix">
													<div className="float-left">
														<strong>3214 Tweets, 63% Offense</strong>
													</div>
													<div className="float-right">
														<small className="text-muted">
															Jun 11, 2020 - Jul 10, 2020
														</small>
													</div>
												</div>
												<Progress
													className="progress-xs"
													color="danger"
													value="63"
												/>
											</td>
											<td className="text-center">
												<strong>Twitter</strong>
											</td>
											<td>
												<div className="small text-muted">Last Tweet</div>
												<strong>Last week</strong>
											</td>
										</tr>
										<tr>
											<td className="text-center">
												<div className="avatar">
													<img
														src={'assets/img/avatars/6.jpg'}
														className="img-avatar"
														alt="admin@bootstrapmaster.com"
													/>
													<span className="avatar-status badge-warning"></span>
												</div>
											</td>
											<td>
												<div>Friderik Dávid</div>
												<div className="small text-muted">
													<span>Neutral</span> | Registered: Jan 1, 2021
												</div>
											</td>
											<td className="text-center">
												<i
													className="flag-icon flag-icon-pl h4 mb-0"
													title="pl"
													id="pl"
												></i>
											</td>
											<td>
												<div className="clearfix">
													<div className="float-left">
														<strong>34556 Tweets, Neutral 53%</strong>
													</div>
													<div className="float-right">
														<small className="text-muted">
															Jun 11, 2020 - Jul 10, 2020
														</small>
													</div>
												</div>
												<Progress
													className="progress-xs"
													color="warning"
													value="53"
												/>
											</td>
											<td className="text-center">
												<strong>Twitter</strong>
											</td>
											<td>
												<div className="small text-muted">Last Tweet</div>
												<strong>Yesterday</strong>
											</td>
										</tr>
									</tbody>
								</Table>
							</CardBody>
						</Card>
					</Col>
				</Row>
			</div>
		);
	}
}

export default Dashboard;
