
module system (
	clk_clk,
	seg7s0_export,
	reset_reset_n,
	seg7s1_export,
	seg7m0_export,
	seg7m1_export,
	seg7h0_export,
	seg7h1_export,
	btsel_export,
	btmode_export,
	btinc_export,
	leds_export,
	uart_rxd,
	uart_txd);	

	input		clk_clk;
	output	[6:0]	seg7s0_export;
	input		reset_reset_n;
	output	[6:0]	seg7s1_export;
	output	[6:0]	seg7m0_export;
	output	[6:0]	seg7m1_export;
	output	[6:0]	seg7h0_export;
	output	[6:0]	seg7h1_export;
	input		btsel_export;
	input		btmode_export;
	input		btinc_export;
	output	[7:0]	leds_export;
	input		uart_rxd;
	output		uart_txd;
endmodule
