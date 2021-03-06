	system u0 (
		.clk_clk       (<connected-to-clk_clk>),       //    clk.clk
		.seg7s0_export (<connected-to-seg7s0_export>), // seg7s0.export
		.reset_reset_n (<connected-to-reset_reset_n>), //  reset.reset_n
		.seg7s1_export (<connected-to-seg7s1_export>), // seg7s1.export
		.seg7m0_export (<connected-to-seg7m0_export>), // seg7m0.export
		.seg7m1_export (<connected-to-seg7m1_export>), // seg7m1.export
		.seg7h0_export (<connected-to-seg7h0_export>), // seg7h0.export
		.seg7h1_export (<connected-to-seg7h1_export>), // seg7h1.export
		.btsel_export  (<connected-to-btsel_export>),  //  btsel.export
		.btmode_export (<connected-to-btmode_export>), // btmode.export
		.btinc_export  (<connected-to-btinc_export>),  //  btinc.export
		.leds_export   (<connected-to-leds_export>),   //   leds.export
		.uart_rxd      (<connected-to-uart_rxd>),      //   uart.rxd
		.uart_txd      (<connected-to-uart_txd>)       //       .txd
	);

