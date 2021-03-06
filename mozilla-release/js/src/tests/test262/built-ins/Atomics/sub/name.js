// |reftest| skip-if(!this.hasOwnProperty('Atomics')) -- Atomics is not enabled unconditionally
// Copyright (C) 2015 André Bargull. All rights reserved.
// Copyright (C) 2017 Mozilla Corporation. All rights reserved.
// This code is governed by the BSD license found in the LICENSE file.

/*---
esid: sec-atomics.sub
description: >
  Atomics.sub.name is "sub".
includes: [propertyHelper.js]
features: [Atomics]
---*/

assert.sameValue(Atomics.sub.name, "sub");

verifyNotEnumerable(Atomics.sub, "name");
verifyNotWritable(Atomics.sub, "name");
verifyConfigurable(Atomics.sub, "name");

reportCompare(0, 0);
