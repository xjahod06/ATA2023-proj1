#!/usr/bin/env python3
"""
Example of usage/test of Cart controller implementation.
"""

import sys
from cartctl import CartCtl, Status as Mode
from cart import Cart, CargoReq, Status as CartStatus
from jarvisenv import Jarvis
import unittest

def log(msg):
    "simple logging"
    print('  %s' % msg)

class TestCartRequests(unittest.TestCase):

    def test_no_prio(self):
        "test 1"

        def add_load(c: CartCtl, cargo_req: CargoReq):
            log('%d: Requesting %s at %s with mode %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src, c.status))
            if c.status != Mode.Idle:
                self.assertEqual(c.status,Mode.Normal)
            c.request(cargo_req)

        def on_move(c: Cart):
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))
            self.assertEqual(c.status,CartStatus.Moving)

        def on_load(c: Cart, cargo_req: CargoReq):
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"
            self.assertGreaterEqual(c.get_free_slot(),1)
            self.assertLessEqual(c.load_sum()+cargo_req.weight,c.load_capacity)
            self.assertEqual(cargo_req.prio,False)

        def on_unload(c: Cart, cargo_req: CargoReq):
            # put some asserts here
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            if cargo_req.content == 'helmet':
                self.assertEqual('B', c.pos)
            if cargo_req.content == 'heart':
                self.assertEqual('A', c.pos)
            if cargo_req.content == 'braceletR':
                self.assertEqual('A', c.pos)
            if cargo_req.content == 'braceletL':
                self.assertEqual('C', c.pos)
        
        # Setup Cart
        # 4 slots, 150 kg max payload capacity, 2=max debug
        cart_dev = Cart(4, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        helmet = CargoReq('A', 'B', 20, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload

        heart = CargoReq('B', 'A', 40, 'heart')
        heart.onload = on_load
        heart.onunload = on_unload

        braceletR = CargoReq('C', 'A', 40, 'braceletR')
        braceletR.onload = on_load
        braceletR.onunload = on_unload

        braceletL = CargoReq('A', 'C', 40, 'braceletL')
        braceletL.onload = on_load
        braceletL.onunload = on_unload

        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(28, add_load, (c,heart))
        Jarvis.plan(42, add_load, (c,helmet))
        Jarvis.plan(56, add_load, (c,braceletL))
        Jarvis.plan(19, add_load, (c,braceletR))
        
        # Exercise + Verify indirect output
        #   SUT is the Cart.
        #   Exercise means calling Cart.request in different time periods.
        #   Requests are called by add_load (via plan and its scheduler).
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        log(cart_dev)
        self.assertTrue(cart_dev.empty())
        self.assertEqual('unloaded', helmet.context)
        self.assertEqual('unloaded', heart.context)
        self.assertEqual('unloaded', braceletR.context)
        self.assertEqual('unloaded', braceletL.context)

    def test_prio(self):
        "test 2"

        def add_load(c: CartCtl, cargo_req: CargoReq):
            log('%d: Requesting %s at %s with mode %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src, c.status))
            if c.status != Mode.Idle:
                self.assertEqual(c.status,Mode.UnloadOnly)
            c.request(cargo_req)

        def on_move(c: Cart):
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))
            self.assertEqual(c.status,CartStatus.Moving)

        def on_load(c: Cart, cargo_req: CargoReq):
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"
            self.assertGreaterEqual(c.get_free_slot(),1)
            self.assertLessEqual(c.load_sum()+cargo_req.weight,c.load_capacity)
            self.assertEqual(cargo_req.prio,True)

        def on_unload(c: Cart, cargo_req: CargoReq):
            # put some asserts here
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            if cargo_req.content == 'helmet':
                self.assertEqual('C', c.pos)
            if cargo_req.content == 'heart':
                self.assertEqual('A', c.pos)
            if cargo_req.content == 'braceletR':
                self.assertEqual('B', c.pos)
            if cargo_req.content == 'braceletL':
                self.assertEqual('A', c.pos)
        
        def check_status(c: CartCtl,status: Mode):
            self.assertEqual(c.status,status)
        
        # Setup Cart
        # 4 slots, 150 kg max payload capacity, 2=max debug
        cart_dev = Cart(4, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        helmet = CargoReq('A', 'C', 20, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload
        helmet.set_priority()

        heart = CargoReq('C', 'A', 40, 'heart')
        heart.onload = on_load
        heart.onunload = on_unload
        heart.set_priority()

        braceletR = CargoReq('A', 'B', 40, 'braceletR')
        braceletR.onload = on_load
        braceletR.onunload = on_unload
        braceletR.set_priority()

        braceletL = CargoReq('B', 'A', 20, 'braceletL')
        braceletL.onload = on_load
        braceletL.onunload = on_unload
        braceletL.set_priority()

        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(61, add_load, (c,helmet))
        Jarvis.plan(81, add_load, (c,heart))
        Jarvis.plan(82, check_status, (c,Mode.UnloadOnly))
        Jarvis.plan(102, add_load, (c,braceletL))
        Jarvis.plan(103, check_status, (c,Mode.UnloadOnly))
        Jarvis.plan(110, add_load, (c,braceletR))
        Jarvis.plan(111, check_status, (c,Mode.UnloadOnly))
        
        # Exercise + Verify indirect output
        #   SUT is the Cart.
        #   Exercise means calling Cart.request in different time periods.
        #   Requests are called by add_load (via plan and its scheduler).
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        log(cart_dev)
        self.assertTrue(cart_dev.empty())
        self.assertEqual('unloaded', helmet.context)
        self.assertEqual('unloaded', heart.context)
        self.assertEqual('unloaded', braceletR.context)
        self.assertEqual('unloaded', braceletL.context)
        
    def test_weight(self):
        "test 3"

        def add_load(c: CartCtl, cargo_req: CargoReq):
            log('%d: Requesting %s at %s with mode %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src, c.status))
            c.request(cargo_req)

        def on_move(c: Cart):
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))
            self.assertEqual(c.status,CartStatus.Moving)

        def on_load(c: Cart, cargo_req: CargoReq):
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"
            #self.assertEqual(cargo_req.prio,True)

        def on_unload(c: Cart, cargo_req: CargoReq):
            # put some asserts here
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            if cargo_req.content == 'helmet':
                self.assertEqual('B', c.pos)
            if cargo_req.content == 'heart':
                self.assertEqual('A', c.pos)
                
        def wait(t: int):
            log('%d: Cart is waiting %is' % (Jarvis.time(),t))
            Jarvis._sleep(t)
        
        def check_status(c: CartCtl,status: Mode):
            self.assertEqual(c.status,status)
        
        # Setup Cart
        # 4 slots, 150 kg max payload capacity, 2=max debug
        cart_dev = Cart(4, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        slowdown = CargoReq('A', 'D', 120, 'slow')
        slowdown.onload = on_load
        slowdown.onunload = on_unload
        
        helmet = CargoReq('C', 'B', 50, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload

        heart = CargoReq('B', 'A', 50, 'heart')
        heart.onload = on_load
        heart.onunload = on_unload

        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(120, add_load, (c,slowdown))
        Jarvis.plan(121, add_load, (c,helmet))
        Jarvis.plan(121, add_load, (c,heart))
        Jarvis.plan(122,wait,(60,))
        Jarvis.plan(255, check_status, (c,Mode.Idle))
        
        # Exercise + Verify indirect output
        #   SUT is the Cart.
        #   Exercise means calling Cart.request in different time periods.
        #   Requests are called by add_load (via plan and its scheduler).
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        log(cart_dev)
        self.assertTrue(cart_dev.empty())
        
    def test_slots(self):
        "test 4"

        def add_load(c: CartCtl, cargo_req: CargoReq):
            log('%d: Requesting %s at %s with mode %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src, c.status))
            c.request(cargo_req)

        def on_move(c: Cart):
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))
            self.assertEqual(c.status,CartStatus.Moving)

        def on_load(c: Cart, cargo_req: CargoReq):
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"
            #self.assertEqual(cargo_req.prio,True)

        def on_unload(c: Cart, cargo_req: CargoReq):
            # put some asserts here
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            if cargo_req.content == 'helmet':
                self.assertEqual('B', c.pos)
            if cargo_req.content == 'heart':
                self.assertEqual('A', c.pos)
                
        def wait(t: int):
            log('%d: Cart is waiting %is' % (Jarvis.time(),t))
            Jarvis._sleep(t)
        
        def check_status(c: CartCtl,status: Mode):
            self.assertEqual(c.status,status)
        
        # Setup Cart
        # 4 slots, 150 kg max payload capacity, 2=max debug
        cart_dev = Cart(1, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        slowdown = CargoReq('A', 'D', 20, 'slow')
        slowdown.onload = on_load
        slowdown.onunload = on_unload
        
        helmet = CargoReq('B', 'A', 50, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload

        heart = CargoReq('C', 'A', 50, 'heart')
        heart.onload = on_load
        heart.onunload = on_unload

        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(120, add_load, (c,slowdown))
        Jarvis.plan(121, add_load, (c,helmet))
        Jarvis.plan(121, add_load, (c,heart))
        Jarvis.plan(122,wait,(60,))
        Jarvis.plan(255, check_status, (c,Mode.Idle))
        
        # Exercise + Verify indirect output
        #   SUT is the Cart.
        #   Exercise means calling Cart.request in different time periods.
        #   Requests are called by add_load (via plan and its scheduler).
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        log(cart_dev)
        self.assertTrue(cart_dev.empty())
        
if __name__ == "__main__":
    unittest.main()
